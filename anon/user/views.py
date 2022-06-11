from . import user
from .. import db
from ..models import User
from .forms import RegForm
from flask import render_template, request, flash, redirect,url_for


@user.route('/', methods=['GET', 'POST'])
def index():
    """The index view function. Confirms staff email and mails them the registration link"""
    return render_template('user/index.html')


@user.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    if request.method == 'POST':
        # registration process
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
        except:
            db.session.rollback()
            db.session.commit()
    return render_template('user/reg.html', form=form)


# @user.route('/confirm')
# def confirmation():
#     """User registration confirmation from link sent to their inbox"""
#     return 'Registration verified.'