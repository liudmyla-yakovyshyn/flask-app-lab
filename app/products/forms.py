from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired


class ProductForm(FlaskForm):
    name = StringField(
        'Назва товару',
        validators=[
            DataRequired(message="Вкажіть назву товару."),
            Length(min=3, message="Назва повинна містити щонайменше 3 символи.")
        ]
    )
    content = TextAreaField(
        'Опис товару',
        render_kw={"rows": 5, "cols": 40},
        validators=[
            DataRequired(message="Введіть опис товару.")
        ]
    )
    price = DecimalField(
        'Ціна ($)',
        places=2,
        validators=[
            DataRequired(message="Вкажіть ціну товару."),
            NumberRange(min=0.01, message="Ціна повинна бути додатною.")
        ]
    )
    category = SelectField(
        'Категорія',
        choices=[
            ('', 'Оберіть категорію...'),
            ('laptops', 'Ноутбуки'),
            ('phones', 'Смартфони'),
            ('pc', 'Комп’ютери'),
            ('gadgets', 'Гаджети'),
            ('accessories', 'Аксесуари')
        ],
        validators=[
            DataRequired(message="Оберіть категорію товару.")
        ]
    )
    quantity = IntegerField(
        'Кількість',
        validators=[
            InputRequired(message="Вкажіть кількість одиниць."),
            NumberRange(min=0, message="Кількість повинна бути невід'ємним числом.")
        ]
    )
    image = FileField(
        'Зображення товару',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png'], 'Дозволені лише формати JPG, JPEG та PNG.')
        ]
    )
    submit = SubmitField('Зберегти')
