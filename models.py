from peewee import *

db = SqliteDatabase('db.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = AutoField()
    name = TextField()
    password = TextField()

class Note(BaseModel):
    id = AutoField()
    name = TextField()
    note = TextField()
    category = TextField()
    user = ForeignKeyField(User, backref='notes')

def init_db():
    db.connect()
#    db.drop_tables([Note, User])
    db.create_tables([Note, User])