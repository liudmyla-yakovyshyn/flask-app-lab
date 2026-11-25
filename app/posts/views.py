from datetime import datetime
from flask import abort, flash, redirect, render_template, request, url_for
from sqlalchemy.orm import joinedload, selectinload
from app import db
from . import post_bp
from .forms import PostForm
from .models import Post, Tag


@post_bp.route("/", strict_slashes=False)
def list_posts():
    stmt = (
        db.select(Post)
        .options(joinedload(Post.user), selectinload(Post.tags))
        .where(Post.is_active == True)
        .order_by(Post.posted.desc())
    )
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", title="Пости", posts=posts)


@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        posted = form.publish_date.data or datetime.utcnow()
        selected_tags = (
            db.session.scalars(db.select(Tag).where(Tag.id.in_(form.tags.data))).all()
            if form.tags.data
            else []
        )
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=posted,
            user_id=form.author_id.data,
            tags=selected_tags,
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
    stmt = (
        db.select(Post)
        .options(joinedload(Post.user), selectinload(Post.tags))
        .where(Post.id == id)
    )
    post = db.session.scalar(stmt)
    if post is None:
        abort(404)
    return render_template("detail_post.html", title=post.title, post=post)


@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    if request.method == "GET":
        form.publish_date.data = post.posted
        form.author_id.data = post.user_id
        form.tags.data = [t.id for t in post.tags]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data or post.posted
        post.user_id = form.author_id.data
        post.tags = (
            db.session.scalars(db.select(Tag).where(Tag.id.in_(form.tags.data))).all()
            if form.tags.data
            else []
        )
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
