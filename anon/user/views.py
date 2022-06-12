from sqlite3 import DatabaseError
from . import user
from .. import db, mail
from ..models import User
from .forms import RegForm
from flask import render_template, request, flash, redirect,url_for, current_app
from flask_mail import Message



@user.route('/', methods=['GET', 'POST'])
def index():
    """The index view function. Confirms staff email and sends them the registration link"""
    if request.method == 'POST':
        # verify staff email
        domain = request.form['email'].split('@')[1]
        valid = current_app.config['STAFF_MAIL_PATTERNS']
        if domain not in valid:
            flash('Invalid email', 'error')
            return redirect(url_for('.index'))
        # send reg link
        msg = Message('Anon Registration', sender=current_app.config['MAIL_USERNAME'], recipients=[request.form['email']])
        msg.body = "Welcome to Anon, here is the registration link, do not share with non staff members\n{}".format(url_for('user.reg', _external=True))
        mail.send(msg)
        flash('Check your inbox for the registration link.', 'info')
        return redirect(url_for('.index'))
    return render_template('user/index.html')


@user.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    if form.validate_on_submit():
        user = User(
            f_name = form.fname.data, l_name = form.lname.data, m_name = form.mname.data, gender = form.gender.data, email = form.email.data,
            phone = form.phone.data, state = form.state.data,
            address = form.address.data, nk_full_name = form.nk_name.data,
            nk_relation = form.nk_relation.data, nk_address = form.nk_address.data, plate_number = form.plate_number.data,
            model = form.model.data, color = form.color.data
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash('User registered successfully ✔', 'success')
            return redirect(url_for('.index'))
        except DatabaseError:
            db.session.rollback()
            db.session.commit()
            flash('A database error has occured, try again.', 'error')
            return redirect(url_for('.index'))
    return render_template('user/reg.html', form=form)