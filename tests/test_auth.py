import unittest
import warnings
from app import create_app, db
from app.users.models import User


class AuthTestCase(unittest.TestCase):

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

        self.existing_user = User(username="olena_27", email="olena@example.com", password="")
        self.existing_user.set_password("secret123")
        db.session.add(self.existing_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_and_login_pages_load(self):
        reg_resp = self.client.get("/users/register")
        self.assertEqual(reg_resp.status_code, 200)
        self.assertIn("Реєстрація".encode("utf-8"), reg_resp.data)

        login_resp = self.client.get("/users/login")
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn("Вхід у систему".encode("utf-8"), login_resp.data)

    def test_register_saves_user_with_hashed_password(self):
        resp = self.client.post(
            "/users/register",
            data={
                "username": "new_user",
                "email": "new@example.com",
                "password": "mypassword",
                "confirm_password": "mypassword",
            },
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        user = db.session.scalar(db.select(User).where(User.email == "new@example.com"))
        self.assertIsNotNone(user)
        self.assertNotEqual(user.password, "mypassword")
        self.assertTrue(user.check_password("mypassword"))

    def test_register_duplicate_email_fails(self):
        resp = self.client.post(
            "/users/register",
            data={
                "username": "another_user",
                "email": "olena@example.com",
                "password": "mypassword",
                "confirm_password": "mypassword",
            },
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("вже існує".encode("utf-8"), resp.data)

    def test_login_account_users_list_and_logout(self):
        unauth_account = self.client.get("/users/account", follow_redirects=False)
        self.assertEqual(unauth_account.status_code, 302)
        self.assertIn("/users/login", unauth_account.location)

        unauth_list = self.client.get("/users/", follow_redirects=False)
        self.assertEqual(unauth_list.status_code, 302)

        login_resp = self.client.post(
            "/users/login",
            data={"email": "olena@example.com", "password": "secret123"},
            follow_redirects=True,
        )
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn("Вітаємо, olena_27!".encode("utf-8"), login_resp.data)

        users_resp = self.client.get("/users/")
        self.assertEqual(users_resp.status_code, 200)
        self.assertIn("Список користувачів (1)".encode("utf-8"), users_resp.data)

        reg_redirect = self.client.get("/users/register", follow_redirects=False)
        self.assertEqual(reg_redirect.status_code, 302)
        self.assertIn("/users/account", reg_redirect.location)

        logout_resp = self.client.get("/users/logout", follow_redirects=True)
        self.assertEqual(logout_resp.status_code, 200)
        self.assertIn("Ви успішно вийшли з системи.".encode("utf-8"), logout_resp.data)

    def test_login_invalid_password(self):
        resp = self.client.post(
            "/users/login",
            data={"email": "olena@example.com", "password": "wrongpassword"},
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Невірний email або пароль.".encode("utf-8"), resp.data)


if __name__ == "__main__":
    unittest.main()
