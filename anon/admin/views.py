from sqlalchemy.exc import DatabaseError
from . import admin
from .. import db
from .forms import SearchForm, Login, EditUser
from ..models import User, Admin
from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required, login_user, logout_user



@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(user_id=form.user_id.data).first()
        if admin is not None and admin.verify_password(form.password.data):
            if not admin.is_active:
                flash('Admin is inactive, please contact the super admin.')
                return redirect(url_for('.login'))
            login_user(admin)
            return redirect(url_for('.admin_index'))
        flash('Invalid login details', 'error')
    return render_template('admin/login.html', form=form)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))


@admin.route('/admin')
@login_required
def admin_index():
    """Index page displays basic stats on platform
    Number of registered users, number of active users and admins and more"""
    users = User.query.all()
    active_admins = len([admin.is_active for admin in Admin.query.all() if admin.is_active])
    active_users = len([user.is_active for user in users if user.is_active])
    return render_template(
        'admin/admin_index.html', users=len(users), active_users=active_users, active_admins=active_admins, user=current_user
    )


@admin.route('/admin/search_users', methods=['GET', 'POST'])
@login_required
def search_users():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.search.data
        return redirect(url_for('.modify_users', query=query))
    return render_template('admin/search_users.html', form=form)


@admin.route('/admin/modify_users/<query>')
@login_required
def modify_users(query):
    users = User.query.all()
    query = query.strip()
    # query is a plate number
    if '@' not in query:
        matches = [user for user in users if user.plate_number.startswith(query)]
    else:
        matches = [user for user in users if user.email.startswith(query)]
    # for user in users:
    #     if user.email and user.email.startswith(query):
    #         matches.append(user)
    return render_template('/admin/modify_users.html', query=query, matches=matches)


@admin.route('/admin/edit_user/<id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get(id)
    form = EditUser()
    if request.method == 'POST':
        user.f_name = form.fname.data
        user.l_name = form.lname.data
        user.m_name = form.mname.data
        user.phone = form.phone.data
        user.state = form.state.data
        user.address = form.address.data
        user.nk_full_name = form.nk_name.data
        user.nk_relation = form.nk_relation.data
        user.nk_address = form.nk_address.data
        user.plate_number = form.plate_number.data
        user.model = form.model.data
        user.color = form.color.data
        try:
            db.session.commit()
            flash('User info updated ✔', 'success')
            return redirect(url_for('.modify_users', query=user.email))
        except DatabaseError:
            flash('A database error has occured.', 'error')
            db.session.rollback()
            db.session.commit()
            return redirect(url_for('.modify_users', query=user.email))
    return render_template('admin/edit_user.html', user=user, form=form)


@admin.route('/admin/modfiy_admins', methods=['GET', 'POST'])
@login_required
def modify_admins():
    admins = [admin for admin in Admin.query.all() if not admin.is_super]
    if request.method == 'POST':
        # do the checking of checked and unchecked boxes for admins
        checked = request.form.getlist('checked')
        active_list = [Admin.query.filter_by(user_id=user_id).first() for user_id in checked]
        try:
            for admin in admins:
                if admin not in active_list:
                    admin.is_active = False
                else:
                    admin.is_active = True
                db.session.add(admin)
            db.session.commit()
            flash('Changes applies successfully ✔', 'success')
            return redirect(url_for('.modify_admins'))
        except DatabaseError:
            db.session.rollback()
            db.session.commit()
            flash('A database error has occured, try again.', 'warning')
            return redirect(url_for('.modify_admins'))
    return render_template('admin/modify_admins.html', admins=admins)