from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Email

class ContactForm(FlaskForm):
    name = StringField("Ім'я", validators=[DataRequired(), Length(min=4, max=10)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Телефон", validators=[DataRequired(), Regexp(r'^\+380\d{9}$', message="Формат: +380XXXXXXXXX")])
    subject = SelectField("Тема", choices=[('general', 'Загальне питання'), ('support', 'Техпідтримка'), ('other', 'Інше')])
    message = TextAreaField("Повідомлення", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Send Message")
