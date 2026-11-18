import logging
import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from .forms import ContactForm

main = Blueprint("main", __name__)

log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "contact.log")

contact_logger = logging.getLogger("contact_logger")
contact_logger.setLevel(logging.INFO)
if not contact_logger.handlers:
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    contact_logger.addHandler(file_handler)


@main.route("/")
@main.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме | Людмила Яковишин")


@main.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        contact_data = {
            "name": form.name.data,
            "email": form.email.data,
            "phone": form.phone.data,
            "subject": form.subject.data,
            "message": form.message.data,
        }
        contact_logger.info(f"Нове повідомлення: {contact_data}")
        flash("Ваше повідомлення успішно надіслано та збережено!", "success")
        return redirect(url_for("main.contacts"))
    elif request.method == "POST":
        flash("Помилка валідації форми. Будь ласка, перевірте введені дані.", "danger")

    return render_template("contacts.html", title="Контакти | Людмила Яковишин", form=form)


@main.route("/homepage")
def home():
    agent = request.user_agent
    return render_template("homepage.html", agent=agent)
