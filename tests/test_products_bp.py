import os
import unittest
import warnings
from unittest.mock import patch
from app import app
from app.products.repository import get_db, add_product

TEST_DB_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "test_products_temp.json")
)


class ProductBlueprintTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings("ignore", category=ResourceWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        cls.db_patcher = patch("app.products.repository.DB_PATH", TEST_DB_FILE)
        cls.db_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.db_patcher.stop()
        if os.path.exists(TEST_DB_FILE):
            try:
                os.remove(TEST_DB_FILE)
            except OSError:
                pass

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

        with get_db() as db:
            db.truncate()

        self.item_id = add_product({
            "name": "Ноутбук Dell Inspiron",
            "content": "Потужний ноутбук для навчання та програмування.",
            "price": "750.00",
            "category": "laptops",
            "quantity": "8"
        })

    def tearDown(self):
        with get_db() as db:
            db.truncate()

    def test_products_list_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ноутбук Dell Inspiron".encode("utf-8"), response.data)
        self.assertIn(b"750.00", response.data)

    def test_product_detail_page(self):
        response = self.client.get(f"/products/{self.item_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ноутбук Dell Inspiron".encode("utf-8"), response.data)
        self.assertIn("Потужний ноутбук для навчання".encode("utf-8"), response.data)

    def test_product_not_found(self):
        response = self.client.get("/products/99999")
        self.assertEqual(response.status_code, 404)

    def test_add_product_success(self):
        payload = {
            "name": "Механічна Клавіатура",
            "content": "Компактна клавіатура з RGB підсвіткою та перемикачами Brown.",
            "price": "85.50",
            "category": "accessories",
            "quantity": "12"
        }
        response = self.client.post("/products/add", data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Механічна Клавіатура".encode("utf-8"), response.data)
        self.assertIn("Товар успішно додано!".encode("utf-8"), response.data)

    def test_add_product_validation_error(self):
        bad_payload = {
            "name": "PC",
            "content": "Опис",
            "price": "-20.00",
            "category": "computers",
            "quantity": "-5"
        }
        response = self.client.post("/products/add", data=bad_payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Мінімум 3 символи".encode("utf-8"), response.data)

    def test_edit_product_success(self):
        edit_payload = {
            "name": "Ноутбук Dell Inspiron Pro",
            "content": "Оновлена конфігурація з SSD 1 ТБ.",
            "price": "820.00",
            "category": "laptops",
            "quantity": "5"
        }
        response = self.client.post(
            f"/products/{self.item_id}/edit",
            data=edit_payload,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ноутбук Dell Inspiron Pro".encode("utf-8"), response.data)
        self.assertIn(b"820.00", response.data)

    def test_delete_product_success(self):
        response = self.client.post(
            f"/products/{self.item_id}/delete",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Ноутбук Dell Inspiron".encode("utf-8"), response.data)
        check_404 = self.client.get(f"/products/{self.item_id}")
        self.assertEqual(check_404.status_code, 404)


if __name__ == "__main__":
    unittest.main()
