from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from string import punctuation, ascii_letters, digits

from models import init_db
from action_db import *

app = Flask(__name__)
app.secret_key = "anything"
init_db()

categories = ['importantly', 'normal']

def is_logged():
    return 'user_name' in session

def current_user():
    name_user = session.get('user_name')
    if not name_user:
        return None
    return get_user_by_name(name_user)

@app.route('/', methods=['GET', 'POST'])
def index():
    if not is_logged():
        return redirect(url_for('login'))

    user = current_user()

    choice_category = None

    if request.method == 'POST':
        name = request.form.get('note_name')
        text = request.form.get('note_text')
        choice_category = request.form.get('category')

        add_note(name, text, choice_category, user.id)

        flash('Note added!', 'success')
        return redirect(url_for('index'))

    notes = get_all_notes(user.id)

    edit_id = request.args.get('edit_id')
    note_to_edit = None
    if edit_id:
        note_to_edit = get_note_by_id(int(edit_id), user.id)

    return render_template('index.html',
                           notes=notes,
                           categories=categories,
                           choice_category=choice_category,
                           note_to_edit=note_to_edit)

@app.route('/delete/<name>')
def delete_note(name):
    user = current_user()
    delete_product(name, user.id)
    flash(f'Note "{name}" deleted!', 'info')
    return redirect(url_for('index'))

@app.route('/update/<note_id>', methods=['GET','POST'])
def update_note(note_id):
    user = current_user()
    note = get_note_by_id(note_id, user.id)

    if note:
        note.name = request.form.get('note_name')
        note.note = request.form.get('note_text')
        note.category = request.form.get('category')

        note.save()

        flash('Note updated!', 'success')

    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    session.pop('user_name', None)
    current_user()
    if request.method == 'POST':
        name = request.form.get('name_user')
        password = request.form.get('password')

        if not name:
            flash('Please enter a name!', 'danger')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('The password must be at least 6 characters long!', 'danger')
            return redirect(url_for('register'))

        has_letter = any(char.isalpha() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special = any(not char.isalnum() for char in password)

        if not has_letter:
            flash('The password must contain at least one letter!', 'danger')
            return redirect(url_for('register'))

        if not has_digit:
            flash('The password must contain at least one digit!', 'danger')
            return redirect(url_for('register'))

        if not has_special:
            flash('The password must contain at least one special character!', 'danger')
            return redirect(url_for('register'))

        if user_exists(name):
            flash('User already exists!', 'danger')
            return redirect(url_for('register'))
        else:
            password_hash = generate_password_hash(password)
            add_user(name, password_hash)

            flash(f'User {name} is registered!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    flash('You leave from system!', 'info')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name_user')
        password = request.form.get('password')

        if not user_exists(name):
            flash(f'User {name} does not exist!', 'danger')
            return redirect(url_for('login'))

        user = get_user_by_name(name)
        if not check_password_hash(user.password, password):
            flash('Password incorrect!', 'danger')
            return redirect(url_for('login'))

        session['user_name'] = user.name
        flash(f'Welcome, {user.name}!', 'info')
        return redirect(url_for('index'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)