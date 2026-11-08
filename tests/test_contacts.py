import os
import unittest
from app import app


class ContactsTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def test_contacts_get(self):
        response = self.client.get("/contacts")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("Надіслати повідомлення", html)
        self.assertIn('name="name"', html)
        self.assertIn('name="email"', html)
        self.assertIn('name="phone"', html)
        self.assertIn('name="subject"', html)
        self.assertIn('name="message"', html)

    def test_contacts_post_valid(self):
        payload = {
            "name": "Людмила",
            "email": "yakovyshyn@example.com",
            "phone": "+380991234567",
            "subject": "general",
            "message": "Тестове повідомлення форми."
        }
        response = self.client.post("/contacts", data=payload, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/contacts", response.location)

        follow_res = self.client.get(response.location)
        self.assertEqual(follow_res.status_code, 200)
        self.assertIn("Ваше повідомлення успішно надіслано та збережено!", follow_res.data.decode("utf-8"))

        log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "logs", "contact.log")
        self.assertTrue(os.path.exists(log_path))
        with open(log_path, "r", encoding="utf-8") as f:
            logs = f.read()
            self.assertIn("yakovyshyn@example.com", logs)

    def test_contacts_invalid_data(self):
        payload = {
            "name": "Li",
            "email": "invalid-email",
            "phone": "0991234567",
            "subject": "",
            "message": ""
        }
        response = self.client.post("/contacts", data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("Довжина імені повинна бути від 4 до 10 символів", html)
        self.assertIn("Формат номера телефону повинен бути: +380XXXXXXXXX", html)
        self.assertIn("Введіть коректну адресу електронної пошти", html)


if __name__ == "__main__":
    unittest.main()

