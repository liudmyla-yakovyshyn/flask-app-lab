from flask import request, render_template, redirect, url_for, flash, session, make_response
from . import users_bp

USERS_DB = {
    "user1": "password123",
    "admin": "admin2026"
}


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("users.profile"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username in USERS_DB and USERS_DB[username] == password:
            session["user"] = username
            flash(f"Успішний вхід! Вітаємо, {username}.", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Wrong data! Try again!", "error")
            return redirect(url_for("users.login"))

    return render_template("login.html")


@users_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Ви успішно вийшли з системи.", "info")
    return redirect(url_for("users.login"))


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
def profile():
    if not session.get("user"):
        flash("Будь ласка, увійдіть у систему для доступу до профілю.", "error")
        return redirect(url_for("users.login"))

    theme = request.cookies.get("theme", "dark")
    return render_template("profile.html", user=session.get("user"), cookies=request.cookies, theme=theme)


@users_bp.route("/cookie/add", methods=["POST"])
def add_cookie():
    if not session.get("user"):
        flash("Доступ заборонено.", "error")
        return redirect(url_for("users.login"))

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
def delete_cookie():
    if not session.get("user"):
        flash("Доступ заборонено.", "error")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    if not key:
        flash("Вкажіть ключ для видалення.", "warning")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key)
    flash(f"Кукі '{key}' успішно видалено!", "info")
    return response


@users_bp.route("/cookie/delete_all", methods=["POST"])
def delete_all_cookies():
    if not session.get("user"):
        flash("Доступ заборонено.", "error")
        return redirect(url_for("users.login"))

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