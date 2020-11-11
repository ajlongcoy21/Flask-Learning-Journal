from flask_wtf import Form
from models import User

from wtforms import StringField, PasswordField, TextAreaField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError(message='User with that name already exists.')

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')

def date_ok(form, field):
    if field.data == None:
        raise ValidationError('Please enter the date in the format mm-dd-yyyy.')

def time_ok(form, field):
    if isinstance(field.data, int):
        raise ValidationError('Please enter an integer for the hours spent.')

class RegisterForm(Form):
    username = StringField( 'Username', validators=[ DataRequired(), 
    Regexp(r'^[a-zA-Z0-9_]+$',message="Username should be one word, letters, numbers, and underscores only."), 
    name_exists ])
    email = StringField('Email', validators=[ DataRequired(), Email(), email_exists ])

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])

    password2 = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired()
        ])

class LoginForm(Form):

    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class EntryForm(Form):

    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', format='%m-%d-%Y', validators=[date_ok])
    time = IntegerField('Time', validators=[], id='time-spent')
    learned = TextAreaField('What I Learned', validators=[DataRequired()], id='what-i-learned')
    resources = TextAreaField('Resources to Remember', validators=[DataRequired()], id='resources-to-remember')

class EditForm(Form):

    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', format='%m-%d-%Y', validators=[date_ok])
    time = IntegerField('Time', validators=[], id='time-spent')
    learned = TextAreaField('What I Learned', validators=[DataRequired()], id='what-i-learned')
    resources = TextAreaField('Resources to Remember', validators=[DataRequired()], id='resources-to-remember')