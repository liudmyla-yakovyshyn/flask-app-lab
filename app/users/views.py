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