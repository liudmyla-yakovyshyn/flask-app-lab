from datetime import datetime
from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms import BooleanField, DateTimeLocalField, SelectField, SelectMultipleField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional
from app import db
from app.users.models import User
from .models import Tag


class PostForm(FlaskForm):
    title = StringField(
        "Заголовок",
        validators=[
            DataRequired(message="Вкажіть заголовок поста."),
            Length(min=2, max=150, message="Заголовок повинен містити від 2 до 150 символів."),
        ],
        render_kw={"placeholder": "Введіть заголовок поста..."},
    )
    content = TextAreaField(
        "Вміст поста",
        validators=[DataRequired(message="Введіть текст поста.")],
        render_kw={"rows": 6, "placeholder": "Напишіть текст публікації..."},
    )
    category = SelectField(
        "Категорія",
        choices=[
            ("news", "Новини"),
            ("publication", "Публікація"),
            ("tech", "Технології"),
            ("other", "Інше"),
        ],
        validators=[DataRequired(message="Оберіть категорію.")],
    )
    publish_date = DateTimeLocalField(
        "Дата публікації",
        format="%Y-%m-%dT%H:%M",
        default=datetime.now,
        validators=[Optional()],
    )
    author_id = SelectField(
        "Автор",
        coerce=int,
        validators=[DataRequired(message="Оберіть автора.")],
    )
    tags = SelectMultipleField("Теги", coerce=int)
    is_active = BooleanField("Активний (відображати на сайті)", default=True)
    submit = SubmitField("Зберегти")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author_id.choices = [
            (u.id, u.username)
            for u in db.session.scalars(select(User).order_by(User.id)).all()
        ]
        self.tags.choices = [
            (t.id, t.name)
            for t in db.session.scalars(select(Tag).order_by(Tag.id)).all()
        ]
