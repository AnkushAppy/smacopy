from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Regexp
from models import User


def user_exist(self,field):
    data = str(field.data)
    username_obj = User.query.get(data.strip())
    if username_obj:
        raise ValidationError('User with the name already exist')


def email_exist(self, field):
    data = str(field.data)
    email_obj = User.query.get(data.strip())
    if email_obj:
        raise ValidationError('email already exist')


class LoginForm(Form):
    username = StringField('Username',
                           validators=[
                               DataRequired(),
                           ])
    password = PasswordField('Password',
                             validators=[
                               DataRequired()
                           ])
    remember_me = BooleanField('Remember Me', default=False)


class RegistrationForm(Form):
    username = StringField('Username',
                           validators=[
                               DataRequired(),
                               Length(max=64),
                               user_exist,
                               Regexp(
                                   r'^[a-zA-Z0-9_]+$',
                                   message=("Username should be at least one word and can only contain "
                                            "Alphabets, Numbers and underscores")
                               )
                           ])
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email(),
                            email_exist
                        ]

    )
    password = PasswordField('Password',
                       validators=[
                           DataRequired(),
                           EqualTo('confirm',message='Password must match'),
                           Length(min=5)
                       ])
    confirm = PasswordField('Confirm Password',
                          validators=[DataRequired()])

