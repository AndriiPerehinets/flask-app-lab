from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SelectMultipleField, SubmitField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length, Optional
from app import db
from app.users.models import User
from app.posts.models import Tag

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
    author_id = SelectField("Author", coerce=int)
    tags = SelectMultipleField("Tags", coerce=int)
    submit = SubmitField("Зберегти пост")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        authors = db.session.scalars(db.select(User).order_by(User.id)).all()
        self.author_id.choices = [(a.id, a.username) for a in authors]
        tags = db.session.scalars(db.select(Tag).order_by(Tag.id)).all()
        self.tags.choices = [(t.id, t.name) for t in tags]
