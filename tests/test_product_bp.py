import unittest
from app import app


class ProductAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def test_products_list_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)

    def test_product_not_found(self):
        response = self.client.get("/products/999999")
        self.assertEqual(response.status_code, 404)

    def test_product_add_get_page(self):
        response = self.client.get("/products/add")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="name"', response.data)

    def test_product_add_validation_error(self):
        response = self.client.post("/products/add", data={"name": "A"})
        self.assertEqual(response.status_code, 200)

    def test_product_edit_not_found(self):
        """Перевірка редагування неіснуючого товару (Update 404)."""
        response = self.client.get("/products/999999/edit")
        self.assertEqual(response.status_code, 404)

    def test_product_delete_not_found(self):
        """Перевірка видалення неіснуючого товару (Delete 404)."""
        response = self.client.post("/products/999999/delete")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
