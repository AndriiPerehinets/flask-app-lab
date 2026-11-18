from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length, Optional

CATEGORIES = [
    ('news', 'Новини (News)'),
    ('publication', 'Публікація (Publication)'),
    ('tech', 'Технології (Tech)'),
    ('other', 'Інше (Other)')
]


class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(min=2, max=150)])
    content = TextAreaField("Основний текст", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField("Активний пост", default=True)
    publish_date = DateTimeLocalField("Дата публікації", format="%Y-%m-%dT%H:%M", default=datetime.now, validators=[Optional()])
    category = SelectField("Категорія", choices=CATEGORIES, default='other', validators=[DataRequired()])
    submit = SubmitField("Зберегти пост")
