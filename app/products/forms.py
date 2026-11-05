from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField("Назва", validators=[DataRequired(), Length(min=3)])
    content = TextAreaField("Опис", validators=[DataRequired()], render_kw={"rows": 5, "cols": 40})
    price = FloatField("Ціна ($)", validators=[DataRequired(), NumberRange(min=0.01)])
    category = SelectField("Категорія", choices=[
        ('electronics', 'Електроніка'),
        ('appliances', 'Побутова техніка'),
        ('other', 'Інше')
    ])
    quantity = IntegerField("Кількість", validators=[NumberRange(min=0)], default=0)
    image = FileField("Зображення", validators=[FileAllowed(['png', 'jpg', 'jpeg'], "Тільки PNG, JPG, JPEG")])
    submit = SubmitField("Зберегти")
