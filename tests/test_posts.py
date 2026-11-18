import unittest
from app import create_app, db
from app.posts.models import Post


class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        """US01: Створення нового поста."""
        with self.app.app_context():
            response = self.client.post("/post/create", data={
                "title": "My first post",
                "content": "This is TDD!",
                "category": "news",
                "is_active": "y"
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post added successfully", response.data)
            post = db.session.scalar(db.select(Post).where(Post.title == "My first post"))
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD!")

    def test_list_posts(self):
        """US02: Перегляд списку всіх постів."""
        with self.app.app_context():
            p = Post(title="Visible Post", content="Post content", is_active=True)
            db.session.add(p)
            db.session.commit()

        response = self.client.get("/post")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Visible Post", response.data)

    def test_view_post_detail(self):
        """US03: Перегляд одного конкретного поста."""
        with self.app.app_context():
            p = Post(title="Detail Test", content="Full description", author="Tester")
            db.session.add(p)
            db.session.commit()
            post_id = p.id

        response = self.client.get(f"/post/{post_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Detail Test", response.data)
        self.assertIn(b"Full description", response.data)

    def test_update_post(self):
        """US04: Редагування поста."""
        with self.app.app_context():
            p = Post(title="Old Title", content="Old Content")
            db.session.add(p)
            db.session.commit()
            post_id = p.id

        response = self.client.post(f"/post/{post_id}/update", data={
            "title": "Updated Title",
            "content": "Updated Content",
            "category": "tech"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post updated successfully", response.data)

        with self.app.app_context():
            updated_post = db.session.get(Post, post_id)
            self.assertEqual(updated_post.title, "Updated Title")

    def test_delete_post(self):
        """US05: Видалення поста."""
        with self.app.app_context():
            p = Post(title="To Delete", content="Will be deleted")
            db.session.add(p)
            db.session.commit()
            post_id = p.id

        response = self.client.post(f"/post/{post_id}/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post deleted successfully", response.data)

        with self.app.app_context():
            deleted_post = db.session.get(Post, post_id)
            self.assertIsNone(deleted_post)

    def test_404_not_found(self):
        """US06: Помилка 404 при неіснуючому пості."""
        response = self.client.get("/post/999999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404", response.data)


if __name__ == "__main__":
    unittest.main()
