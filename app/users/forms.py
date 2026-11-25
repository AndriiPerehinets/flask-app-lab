from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from app import db
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=4, max=16),
            Regexp(
                r'^[A-Za-z][A-Za-z0-9_.]*$',
                message='Username must start with a letter and contain only letters, numbers, dots or underscores.'
            )
        ]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = db.session.scalars(db.select(User).where(User.email == email.data)).first()
        if user:
            raise ValidationError('Email is already registered.')

    def validate_username(self, username):
        user = db.session.scalars(db.select(User).where(User.username == username.data)).first()
        if user:
            raise ValidationError('Username is already taken.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
