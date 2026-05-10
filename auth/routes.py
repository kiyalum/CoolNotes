from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from action_db import *

auth_bp = Blueprint('auth', __name__, template_folder='templates')

def current_user():
    name_user = session.get('user_name')
    if not name_user:
        return None
    return get_user_by_name(name_user)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    session.pop('user_name', None)
    current_user()
    if request.method == 'POST':
        name = request.form.get('name_user')
        password = request.form.get('password')

        if not name:
            flash('Please enter a name!', 'danger')
            return redirect(url_for('auth.register'))

        if len(password) < 6:
            flash('The password must be at least 6 characters long!', 'danger')
            return redirect(url_for('auth.register'))

        has_letter = any(char.isalpha() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special = any(not char.isalnum() for char in password)

        if not has_letter:
            flash('The password must contain at least one letter!', 'danger')
            return redirect(url_for('auth.register'))

        if not has_digit:
            flash('The password must contain at least one digit!', 'danger')
            return redirect(url_for('auth.register'))

        if not has_special:
            flash('The password must contain at least one special character!', 'danger')
            return redirect(url_for('auth.register'))

        if user_exists(name):
            flash('User already exists!', 'danger')
            return redirect(url_for('auth.register'))
        else:
            password_hash = generate_password_hash(password)
            add_user(name, password_hash)

            flash(f'User {name} is registered!', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_name', None)
    flash('You leave from system!', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name_user')
        password = request.form.get('password')

        if not user_exists(name):
            flash(f'User {name} does not exist!', 'danger')
            return redirect(url_for('auth.login'))

        user = get_user_by_name(name)
        if not check_password_hash(user.password, password):
            flash('Password incorrect!', 'danger')
            return redirect(url_for('auth.login'))

        session['user_name'] = user.name
        flash(f'Welcome, {user.name}!', 'info')
        return redirect(url_for('notes.index'))

    return render_template('auth/login.html')