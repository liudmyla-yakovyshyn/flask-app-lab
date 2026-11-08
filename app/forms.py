from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, TelField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(message="Поле 'Name' обов'язкове для заповнення."),
            Length(min=4, max=10, message="Довжина імені повинна бути від 4 до 10 символів.")
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Поле 'Email' обов'язкове для заповнення."),
            Email(message="Введіть коректну адресу електронної пошти.")
        ]
    )
    phone = TelField(
        'Phone',
        validators=[
            DataRequired(message="Поле 'Phone' обов'язкове для заповнення."),
            Regexp(r'^\+380\d{9}$', message="Формат номера телефону повинен бути: +380XXXXXXXXX")
        ]
    )
    subject = SelectField(
        'Subject',
        choices=[
            ('', 'Оберіть тему звернення...'),
            ('general', 'Загальні питання'),
            ('cooperation', 'Співпраця та пропозиції'),
            ('support', 'Технічна підтримка'),
            ('feedback', 'Відгук про резюме/проєкт')
        ],
        validators=[
            DataRequired(message="Будь ласка, оберіть тему зі списку.")
        ]
    )
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message="Поле 'Message' обов'язкове для заповнення."),
            Length(max=500, message="Повідомлення не повинно перевищувати 500 символів.")
        ]
    )
    submit = SubmitField('Send Message')
