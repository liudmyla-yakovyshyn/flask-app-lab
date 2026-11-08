import os
import uuid
from datetime import datetime
from tinydb import TinyDB, Query

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data",
    "products.json"
)


def get_db(path=None):
    target = path or DB_PATH
    os.makedirs(os.path.dirname(target), exist_ok=True)
    return TinyDB(target)


def get_all_products(db_path=None):
    with get_db(db_path) as db:
        return sorted(db.all(), key=lambda item: item.get("id", 0))


def get_product(product_id: int, db_path=None):
    with get_db(db_path) as db:
        Product = Query()
        return db.get(Product.id == product_id)


def save_image_file(image_field, upload_dir):
    if not image_field or not getattr(image_field, "filename", None):
        return None
    ext = os.path.splitext(image_field.filename)[1].lower()
    file_name = f"{uuid.uuid4().hex}{ext}"
    os.makedirs(upload_dir, exist_ok=True)
    image_field.save(os.path.join(upload_dir, file_name))
    return f"uploads/{file_name}"


def add_product(data, image_field=None, upload_dir=None, db_path=None):
    with get_db(db_path) as db:
        items = db.all()
        next_id = max((item.get("id", 0) for item in items), default=0) + 1
        image_path = save_image_file(image_field, upload_dir) if upload_dir else None

        record = {
            "id": next_id,
            "name": str(data["name"]).strip(),
            "content": str(data["content"]).strip(),
            "price": float(data["price"]),
            "category": data["category"],
            "quantity": int(data["quantity"]),
            "image": image_path or data.get("image"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        db.insert(record)
        return next_id


def edit_product(product_id: int, data, image_field=None, upload_dir=None, db_path=None):
    with get_db(db_path) as db:
        Product = Query()
        current = db.get(Product.id == product_id)
        if not current:
            return False

        image_path = current.get("image")
        if image_field and getattr(image_field, "filename", None) and upload_dir:
            uploaded = save_image_file(image_field, upload_dir)
            if uploaded:
                image_path = uploaded

        db.update({
            "name": str(data["name"]).strip(),
            "content": str(data["content"]).strip(),
            "price": float(data["price"]),
            "category": data["category"],
            "quantity": int(data["quantity"]),
            "image": image_path
        }, Product.id == product_id)
        return True


def remove_product(product_id: int, db_path=None):
    with get_db(db_path) as db:
        Product = Query()
        deleted = db.remove(Product.id == product_id)
        return bool(deleted)
