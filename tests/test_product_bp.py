import unittest
from app import app

class ProductAppTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування клієнта тестування для продуктів."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_list_page(self):
        """Тест головної сторінки каталогу товарів /products/."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Phone", response.data)

    def test_product_detail_page(self):
        """Тест детальної сторінки конкретного товару за ID (/products/1)."""
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200", response.data)

    def test_product_not_found(self):
        """Тест перевірки помилки 404, якщо товару з таким ID не існує."""
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()