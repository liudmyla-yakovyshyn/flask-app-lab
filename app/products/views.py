import os
from flask import render_template, abort, redirect, url_for, flash, request
from . import products_bp
from .forms import ProductForm
from .repository import (
    get_all_products,
    get_product,
    add_product,
    edit_product,
    remove_product
)


def get_upload_dir():
    return os.path.join(os.path.dirname(__file__), "static", "uploads")


@products_bp.route("/")
def list_products():
    items = get_all_products()
    return render_template("products.html", products=items)


@products_bp.route("/add", methods=["GET", "POST"], endpoint="add_product")
def add_product_view():
    form = ProductForm()
    if form.validate_on_submit():
        add_product(form.data, form.image.data, get_upload_dir())
        flash("Товар успішно додано!", "success")
        return redirect(url_for("products.list_products"))
    elif request.method == "POST":
        flash("Помилка при заповненні форми товару. Перевірте поля.", "danger")

    return render_template("add_product.html", form=form)


@products_bp.route("/<int:product_id>")
def detail_product(product_id):
    product = get_product(product_id)
    if product is None:
        abort(404)
    return render_template("detail_product.html", product=product)


@products_bp.route("/<int:product_id>/edit", methods=["GET", "POST"], endpoint="edit_product")
def edit_product_view(product_id):
    product = get_product(product_id)
    if product is None:
        abort(404)

    form = ProductForm()
    if form.validate_on_submit():
        edit_product(product_id, form.data, form.image.data, get_upload_dir())
        flash("Товар успішно оновлено!", "success")
        return redirect(url_for("products.detail_product", product_id=product_id))
    elif request.method == "POST":
        flash("Помилка валідації форми редагування.", "danger")
    elif request.method == "GET":
        form.name.data = product.get("name", "")
        form.content.data = product.get("content", "")
        form.price.data = product.get("price", 0.0)
        form.category.data = product.get("category", "")
        form.quantity.data = product.get("quantity", 0)

    return render_template("edit_product.html", form=form, product=product)


@products_bp.route("/<int:product_id>/delete", methods=["POST"], endpoint="delete_product")
def delete_product_view(product_id):
    product = get_product(product_id)
    if product is None:
        abort(404)

    remove_product(product_id)
    flash("Товар успішно видалено!", "warning")
    return redirect(url_for("products.list_products"))
