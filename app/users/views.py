from flask import flash, make_response, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import db
from . import users_bp
from .forms import LoginForm, RegistrationForm
from .models import User


@users_bp.route("/", strict_slashes=False)
@login_required
def users_list():
    users = db.session.scalars(db.select(User).order_by(User.id)).all()
    return render_template("users_list.html", title="Користувачі", users=users)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password="",
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Акаунт для {form.username.data} успішно створено!", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html", title="Реєстрація", form=form)


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.email == form.email.data))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Вітаємо, {user.username}! Ви успішно увійшли.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("users.account"))
        flash("Невірний email або пароль.", "danger")

    return render_template("login.html", title="Вхід", form=form)


@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви успішно вийшли з системи.", "info")
    return redirect(url_for("users.login"))


@users_bp.route("/account")
@login_required
def account():
    return render_template("account.html", title="Акаунт", user=current_user)


@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("hi.html", name=name, age=age)


@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)


@users_bp.route("/profile")
@login_required
def profile():
    theme = request.cookies.get("theme", "dark")
    return render_template("profile.html", user=current_user.username, cookies=request.cookies, theme=theme)


@users_bp.route("/cookie/add", methods=["POST"])
@login_required
def add_cookie():
    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()
    max_age = request.form.get("max_age", type=int)

    if not key:
        flash("Ключ кукі не може бути порожнім.", "warning")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(key, value, max_age=max_age if max_age and max_age > 0 else None)
    flash(f"Кукі '{key}' успішно додано!", "success")
    return response


@users_bp.route("/cookie/delete", methods=["POST"])
@login_required
def delete_cookie():
    key = request.form.get("key", "").strip()
    if not key:
        flash("Вкажіть ключ для видалення.", "warning")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key)
    flash(f"Кукі '{key}' успішно видалено!", "info")
    return response


@users_bp.route("/cookie/delete_all", methods=["POST"])
@login_required
def delete_all_cookies():
    response = make_response(redirect(url_for("users.profile")))
    for key in request.cookies:
        response.delete_cookie(key)
    flash("Усі кукі успішно видалено!", "info")
    return response

@users_bp.route("/theme/<string:theme>")
def set_theme(theme):
    if theme not in ["light", "dark"]:
        theme = "dark"
    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("theme", theme, max_age=30 * 24 * 60 * 60)
    flash(f"Встановлено {theme} тему.", "info")
    return response