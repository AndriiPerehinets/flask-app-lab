from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

# Підтримка Email валідатора з безпечним fallback, якщо не встановлений email-validator
try:
    from wtforms.validators import Email
    _test = Email()
except Exception:
    def Email(message="Некоректний формат email адреси"):
        return Regexp(r'^[\w\.-]+@[\w\.-]+\.\w+$', message=message)


class ContactForm(FlaskForm):
    """
    WTF-форма для зв'язку .
    Вимоги до полів:
    - name: Обов'язкове, довжина min=4, max=10
    - email: Обов'язкове, пошта
    - phone: Формат +380?????????
    - subject: SelectField із випадаючим списком тем
    - message: Обов'язкове, довжина до 500 символів
    """
    name = StringField(
        "Ім'я",
        validators=[
            DataRequired(message="Поле ім'я є обов'язковим"),
            Length(min=4, max=10, message="Довжина імені повинна бути від 4 до 10 символів")
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Поле email є обов'язковим"),
            Email(message="Введіть коректну адресу електронної пошти")
        ]
    )
    phone = StringField(
        "Телефон",
        validators=[
            DataRequired(message="Поле телефону є обов'язковим"),
            Regexp(r'^\+380\d{9}$', message="Формат телефону повинен бути +380XXXXXXXXX (наприклад, +380501234567)")
        ]
    )
    subject = SelectField(
        "Тема",
        choices=[
            ('', '-- Оберіть тему звернення --'),
            ('general', 'Загальні питання'),
            ('support', 'Технічна підтримка'),
            ('partnership', 'Співпраця та партнерство'),
            ('feedback', 'Відгуки та пропозиції')
        ],
        validators=[
            DataRequired(message="Будь ласка, оберіть тему повідомлення")
        ]
    )
    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Поле повідомлення є обов'язковим"),
            Length(max=500, message="Довжина повідомлення не повинна перевищувати 500 символів")
        ]
    )
    submit = SubmitField("Send Message")

