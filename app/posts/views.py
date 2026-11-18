from datetime import datetime
from flask import flash, redirect, render_template, request, session, url_for
from app import db
from . import post_bp
from .forms import PostForm
from .models import Post


@post_bp.route("/", strict_slashes=False)
def list_posts():
    stmt = db.select(Post).where(Post.is_active == True).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", title="Пости", posts=posts)


@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        author = session.get("user") or "Anonymous"
        posted = form.publish_date.data or datetime.utcnow()
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=posted,
            author=author,
        )
        db.session.add(post)
        db.session.commit()
        flash("Пост успішно створено!", "success")
        return redirect(url_for("posts.list_posts"))
    elif request.method == "POST":
        flash("Помилка валідації форми. Перевірте введені дані.", "danger")

    return render_template("add_post.html", title="Створити пост", form=form, is_edit=False)


@post_bp.route("/<int:id>")
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template("detail_post.html", title=post.title, post=post)


@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    if request.method == "GET":
        form.publish_date.data = post.posted

    if form.validate_on_submit():
        form.populate_obj(post)
        post.posted = form.publish_date.data or post.posted
        db.session.commit()
        flash("Пост успішно оновлено!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))
    elif request.method == "POST":
        flash("Помилка при оновленні поста. Перевірте поля форми.", "danger")

    return render_template("add_post.html", title="Редагувати пост", form=form, post=post, is_edit=True)


@post_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Пост успішно видалено!", "success")
        return redirect(url_for("posts.list_posts"))

    return render_template("delete_confirm.html", title="Видалення поста", post=post)
