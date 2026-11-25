import unittest
from app import create_app, db, bcrypt
from app.users.models import User


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_and_login_pages_load(self):
        """Перевірка коректного завантаження сторінок реєстрації та входу."""
        res_register = self.client.get("/users/register")
        self.assertEqual(res_register.status_code, 200)
        self.assertIn(b"Register", res_register.data)

        res_login = self.client.get("/users/login")
        self.assertEqual(res_login.status_code, 200)
        self.assertIn(b"Login", res_login.data)

    def test_register_saves_user_to_db(self):
        """Тестування збереження користувача у БД при реєстрації."""
        response = self.client.post("/users/register", data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Account created for testuser!", response.data)

        with self.app.app_context():
            user = db.session.scalar(db.select(User).where(User.email == "testuser@example.com"))
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "testuser")
            self.assertTrue(user.check_password("password123"))

    def test_login_and_logout(self):
        """Тестування входу і виходу користувача на сайті."""
        with self.app.app_context():
            hashed = bcrypt.generate_password_hash("secret123").decode("utf-8")
            user = User(username="loginuser", email="login@example.com", password=hashed)
            db.session.add(user)
            db.session.commit()

        # Вхід
        res_login = self.client.post("/users/login", data={
            "email": "login@example.com",
            "password": "secret123"
        }, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)
        self.assertIn(b"Welcome, loginuser!", res_login.data)

        # Доступ до захищеної сторінки списку користувачів
        res_list = self.client.get("/users/list")
        self.assertEqual(res_list.status_code, 200)

        # Вихід
        res_logout = self.client.get("/users/logout", follow_redirects=True)
        self.assertEqual(res_logout.status_code, 200)
        self.assertIn(b"You have successfully logged out.", res_logout.data)

        # Після виходу /users/account має перенаправляти на вхід
        res_account = self.client.get("/users/account")
        self.assertEqual(res_account.status_code, 302)


if __name__ == "__main__":
    unittest.main()
