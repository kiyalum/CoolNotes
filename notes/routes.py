from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from action_db import *

notes_bp = Blueprint('notes', __name__, template_folder='templates')

categories = ['importantly', 'normal']

def is_logged():
    return 'user_name' in session

def current_user():
    name_user = session.get('user_name')
    if not name_user:
        return None
    return get_user_by_name(name_user)

@notes_bp.route('/', methods=['GET', 'POST'])
def index():
    if not is_logged():
        return redirect(url_for('auth.login'))

    user = current_user()

    choice_category = None

    if request.method == 'POST':
        name = request.form.get('note_name')
        text = request.form.get('note_text')
        choice_category = request.form.get('category')

        add_note(name, text, choice_category, user.id)

        flash('Note added!', 'success')
        return redirect(url_for('notes.index'))

    notes = get_all_notes(user.id)

    edit_id = request.args.get('edit_id')
    note_to_edit = None
    if edit_id:
        note_to_edit = get_note_by_id(int(edit_id), user.id)

    return render_template('notes/index.html',
                           notes=notes,
                           categories=categories,
                           choice_category=choice_category,
                           note_to_edit=note_to_edit)

@notes_bp.route('/delete/<name>')
def delete_note(name):
    user = current_user()
    delete_product(name, user.id)
    flash(f'Note "{name}" deleted!', 'info')
    return redirect(url_for('notes.index'))

@notes_bp.route('/update/<note_id>', methods=['GET','POST'])
def update_note(note_id):
    user = current_user()
    note = get_note_by_id(note_id, user.id)

    if note:
        note.name = request.form.get('note_name')
        note.note = request.form.get('note_text')
        note.category = request.form.get('category')

        note.save()

        flash('Note updated!', 'success')

    return redirect(url_for('notes.index'))