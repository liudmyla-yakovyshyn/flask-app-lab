from flask import render_template, abort
from . import products_bp

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 1200,
        "content": "Ноутбук для веб-розробки: Core i7, 16 ГБ RAM, 512 ГБ SSD."
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 800,
        "content": "Смартфон для тестування мобільної верстки: OLED 6.5, 5000 мА·год."
    },
    {
        "id": 3,
        "name": "PC",
        "price": 1800,
        "content": "Робоча станція для рендерингу та дизайну у Figma: RTX 4070, 32 ГБ RAM."
    }
]


@products_bp.route("/")
def list_products():
    return render_template("products.html", products=products)


@products_bp.route("/<int:product_id>")
def detail_product(product_id):
    product = next((item for item in products if item["id"] == product_id), None)
    if product is None:
        abort(404)
    return render_template("detail_product.html", product=product)