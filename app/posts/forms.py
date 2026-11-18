from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeLocalField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


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
    is_active = BooleanField("Активний (відображати на сайті)", default=True)
    submit = SubmitField("Зберегти")

