from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError
from app import db
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Ім'я користувача",
        validators=[
            DataRequired(message="Вкажіть ім'я користувача."),
            Length(min=4, max=16, message="Ім'я повинно містити від 4 до 16 символів."),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                message="Ім'я повинно починатися з літери та містити лише латинські літери, цифри, крапки або підкреслення.",
            ),
        ],
        render_kw={"placeholder": "username"},
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Вкажіть електронну пошту."),
            Email(message="Некоректний формат електронної пошти."),
        ],
        render_kw={"placeholder": "user@example.com"},
    )
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(message="Введіть пароль."),
            Length(min=6, message="Пароль повинен містити щонайменше 6 символів."),
        ],
        render_kw={"placeholder": "Мінімум 6 символів"},
    )
    confirm_password = PasswordField(
        "Підтвердження пароля",
        validators=[
            DataRequired(message="Підтвердіть пароль."),
            EqualTo("password", message="Паролі не співпадають."),
        ],
        render_kw={"placeholder": "Повторіть пароль"},
    )
    submit = SubmitField("Зареєструватися")

    def validate_username(self, field):
        user = db.session.scalar(db.select(User).where(User.username == field.data))
        if user:
            raise ValidationError("Користувач із таким іменем вже існує.")

    def validate_email(self, field):
        user = db.session.scalar(db.select(User).where(User.email == field.data))
        if user:
            raise ValidationError(f"Користувач з таким емейлом {field.data} вже існує.")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Вкажіть електронну пошту."),
            Email(message="Некоректний формат електронної пошти."),
        ],
        render_kw={"placeholder": "user@example.com"},
    )
    password = PasswordField(
        "Пароль",
        validators=[DataRequired(message="Введіть пароль.")],
        render_kw={"placeholder": "Введіть пароль"},
    )
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField("Увійти")
