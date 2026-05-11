from models import Note, User

'''Нотатки'''
# отримання
def get_all_notes(user_id: int):
    return Note.select().where(Note.user == user_id).order_by(Note.category.asc())

def get_note_by_id(note_id: int, user_id: int):
    return Note.get_or_none(Note.id == note_id, Note.user == user_id)

# додавання
def add_note(note_name: str, note_text: str, note_category: str, user_id: int):
    Note.create(name=note_name, note=note_text, category=note_category, user_id=user_id)

# видалення
def delete_product(note_id: str, user_id: int):
    Note.delete().where((Note.user == user_id) & (Note.id == note_id)).execute()

'''Юзер'''
# додавання
def add_user(name: str, password: str):
    User.create(name=name, password=password)

def user_exists(name: str) -> bool:
    return User.select().where(User.name == name).exists()

def get_user_by_name(name: str):
    return User.get_or_none(User.name == name)