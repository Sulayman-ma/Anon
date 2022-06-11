import re
from . import admin
from .forms import SearchForm, Login
from ..models import User, Admin
from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required, login_user, logout_user



@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(user_id=form.user_id.data).first()
        if admin is not None and admin.verify_password(form.password.data):
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


def query_users(query):
    users = User.query.all()
    matches = [user for user in users if query in user.email]
    return matches

def search_users(query):
    return

@admin.route('/admin/modify_users', methods=['GET', 'POST'])
@login_required
def modify_users():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.search.data
        return redirect(url_for('.modify_results', query=query))
    return render_template('admin/modify_users.html', form=form)


@admin.route('/admin/modify_results/<query>', methods=['GET', 'POST'])
@login_required
def modify_results(query):
    form = SearchForm()
    matches = query_users(query)
    return render_template('/admin/modify_results.html', form=form, query=query, matches=matches)


@admin.route('/admin/modfiy_admins')
@login_required
def modify_admins():
    admins = [admin for admin in Admin.query.all() if not admin.is_super]
    return render_template('admin/modify_admins.html', admins=admins)