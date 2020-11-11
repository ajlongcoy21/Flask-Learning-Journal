import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from peewee import *

DATABASE = SqliteDatabase('journal.db')

class User(UserMixin, Model):
    id = IntegerField(primary_key=True)
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    def get_entries(self):
        return Entry.select().where(Entry.user == self)

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        """
        Create instance of a user in the database
        """
        try:
            with DATABASE.transaction():
                cls.create(
                    username = username,
                    email = email,
                    password = generate_password_hash(password),
                    is_admin = admin
                )
        except IntegrityError:
            raise ValueError("User already exists")

class Entry(Model):
    id = IntegerField(primary_key=True)
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField( User, related_name='entries')
    title = CharField()
    date = DateField()
    time = IntegerField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry], safe=True)
    DATABASE.close()