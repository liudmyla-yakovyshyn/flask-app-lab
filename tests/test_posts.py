import unittest
import warnings
from datetime import datetime
from app import create_app, db
from app.posts.models import Post


class PostsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings("ignore", category=ResourceWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)

    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.sample_post = Post(
            title="Тестова публікація",
            content="Це повний текст тестового поста для перевірки CRUD операцій.",
            category="tech",
            is_active=True,
            author="Tester",
            posted=datetime(2026, 11, 18, 12, 0),
        )
        db.session.add(self.sample_post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_posts_list_page(self):
        inactive_post = Post(
            title="Прихований пост",
            content="Цей пост не повинен відображатися у списку.",
            category="other",
            is_active=False,
        )
        db.session.add(inactive_post)
        db.session.commit()

        response = self.client.get("/post")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестова публікація".encode("utf-8"), response.data)
        self.assertNotIn("Прихований пост".encode("utf-8"), response.data)

    def test_post_detail_page(self):
        response = self.client.get(f"/post/{self.sample_post.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестова публікація".encode("utf-8"), response.data)
        self.assertIn("Tester".encode("utf-8"), response.data)

    def test_post_not_found(self):
        response = self.client.get("/post/99999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Сторінку не знайдено".encode("utf-8"), response.data)

    def test_create_post_anonymous(self):
        payload = {
            "title": "Нова новина",
            "content": "Зміст нової публікації у системі.",
            "category": "news",
            "publish_date": "2026-11-18T14:30",
            "is_active": "y",
        }
        response = self.client.post("/post/create", data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Нова новина".encode("utf-8"), response.data)

        created = db.session.scalar(db.select(Post).where(Post.title == "Нова новина"))
        self.assertIsNotNone(created)
        self.assertEqual(created.author, "Anonymous")

    def test_create_post_with_session_user(self):
        with self.client.session_transaction() as sess:
            sess["user"] = "liudmyla"

        payload = {
            "title": "Авторський пост",
            "content": "Пост від авторизованого користувача.",
            "category": "publication",
            "publish_date": "2026-11-18T15:00",
            "is_active": "y",
        }
        response = self.client.post("/post/create", data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        created = db.session.scalar(db.select(Post).where(Post.title == "Авторський пост"))
        self.assertIsNotNone(created)
        self.assertEqual(created.author, "liudmyla")

    def test_create_post_validation_error(self):
        bad_payload = {
            "title": "A",
            "content": "Текст поста",
            "category": "news",
        }
        response = self.client.post("/post/create", data=bad_payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("від 2 до 150 символів".encode("utf-8"), response.data)

    def test_update_post_get_and_post(self):
        get_resp = self.client.get(f"/post/{self.sample_post.id}/update")
        self.assertEqual(get_resp.status_code, 200)
        self.assertIn("2026-11-18T12:00".encode("utf-8"), get_resp.data)

        update_payload = {
            "title": "Оновлений заголовок поста",
            "content": "Оновлений зміст поста після редагування.",
            "category": "publication",
            "publish_date": "2026-11-18T16:45",
            "is_active": "y",
        }
        post_resp = self.client.post(
            f"/post/{self.sample_post.id}/update",
            data=update_payload,
            follow_redirects=True,
        )
        self.assertEqual(post_resp.status_code, 200)
        self.assertIn("Оновлений заголовок поста".encode("utf-8"), post_resp.data)

        updated = db.session.get(Post, self.sample_post.id)
        self.assertEqual(updated.category, "publication")

    def test_delete_post_get_confirm_and_post(self):
        confirm_resp = self.client.get(f"/post/{self.sample_post.id}/delete")
        self.assertEqual(confirm_resp.status_code, 200)
        self.assertIn("Підтвердження видалення".encode("utf-8"), confirm_resp.data)

        del_resp = self.client.post(
            f"/post/{self.sample_post.id}/delete",
            follow_redirects=True,
        )
        self.assertEqual(del_resp.status_code, 200)
        self.assertNotIn("Тестова публікація".encode("utf-8"), del_resp.data)
        self.assertIsNone(db.session.get(Post, self.sample_post.id))


if __name__ == "__main__":
    unittest.main()

