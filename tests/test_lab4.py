import unittest
import warnings
from app import create_app, db
from app.users.models import User


class Lab4TestCase(unittest.TestCase):

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

        user = User(username="user1", email="user1@example.com", password="")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_unauthorized_profile_redirects_to_login(self):
        response = self.client.get("/users/profile", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login", response.location)

    def test_login_success_and_logout(self):
        response = self.client.post(
            "/users/login",
            data={"email": "user1@example.com", "password": "password123"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user1", response.data)

        response_logout = self.client.get("/users/logout", follow_redirects=True)
        self.assertEqual(response_logout.status_code, 200)
        self.assertIn("Вхід".encode("utf-8"), response_logout.data)

    def test_add_cookie_flow(self):
        with self.client:
            self.client.post(
                "/users/login",
                data={"email": "user1@example.com", "password": "password123"},
            )
            response = self.client.post(
                "/users/cookie/add",
                data={"key": "test_token", "value": "abc456", "max_age": 3600},
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"test_token", response.data)

    def test_theme_cookie_selection(self):
        with self.client:
            self.client.post(
                "/users/login",
                data={"email": "user1@example.com", "password": "password123"},
            )
            response = self.client.get("/users/theme/light", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"theme", response.data)


if __name__ == "__main__":
    unittest.main()
