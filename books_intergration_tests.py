# Integration tests for books tab
# Author: Kai Francis
# Date: December 3, 2024

import unittest
import json
from api import app
import books

class TestBooksIntegration(unittest.TestCase):
    def setUp(self):
        """Setting up the test client and configuring the test database."""
        self.app = app.test_client()
        self.app.testing = True

        # Using a test database for integration testing
        books.DATABASE = 'test_books.db'
        with books.sqlite3.connect(books.DATABASE) as conn:
            cursor = conn.cursor()
            # Create the books table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    genre TEXT NOT NULL
                )
            ''')
            # Create the reviews table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    note TEXT NOT NULL,
                    FOREIGN KEY (book_id) REFERENCES books (id)
                )
            ''')
            conn.commit()

    def tearDown(self):
        """Cleaning up the test database after each test."""
        with books.sqlite3.connect(books.DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('DROP TABLE IF EXISTS reviews')
            cursor.execute('DROP TABLE IF EXISTS books')
            conn.commit()

    def test_add_book(self):
        """Testing the POST /books endpoint."""
        response = self.app.post(
            '/books',
            data=json.dumps({"title": "To Kill a Mockingbird", "genre": "Fiction"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("Book 'To Kill a Mockingbird' added successfully.", response.get_data(as_text=True))

    def test_add_review(self):
        """Testing the POST /books/<int:book_id>/reviews endpoint."""
        # First, adding a book
        self.app.post(
            '/books',
            data=json.dumps({"title": "To Kill a Mockingbird", "genre": "Fiction"}),
            content_type='application/json'
        )
        # Then, adding a review
        response = self.app.post(
            '/books/1/reviews',
            data=json.dumps({"rating": 5, "note": "A masterpiece!"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("Review added to book ID 1.", response.get_data(as_text=True))

    def test_edit_review(self):
        """Testing the PUT /books/<int:book_id>/reviews/<int:review_id> endpoint."""
        # Adding a book and a review
        self.app.post(
            '/books',
            data=json.dumps({"title": "To Kill a Mockingbird", "genre": "Fiction"}),
            content_type='application/json'
        )
        self.app.post(
            '/books/1/reviews',
            data=json.dumps({"rating": 4, "note": "Good book"}),
            content_type='application/json'
        )
        # Editing the review
        response = self.app.put(
            '/books/1/reviews/1',
            data=json.dumps({"rating": 5, "note": "An excellent book!"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Review ID 1 for book ID 1 updated.", response.get_data(as_text=True))

    def test_delete_review(self):
        """Testing the DELETE /books/<int:book_id>/reviews/<int:review_id> endpoint."""
        # Adding a book and a review
        self.app.post(
            '/books',
            data=json.dumps({"title": "To Kill a Mockingbird", "genre": "Fiction"}),
            content_type='application/json'
        )
        self.app.post(
            '/books/1/reviews',
            data=json.dumps({"rating": 5, "note": "A masterpiece!"}),
            content_type='application/json'
        )
        # Deleting the review
        response = self.app.delete('/books/1/reviews/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Review ID 1 deleted from book ID 1.", response.get_data(as_text=True))

    def test_delete_book(self):
        """Testing the DELETE /books/<int:book_id> endpoint."""
        # Adding a book
        self.app.post(
            '/books',
            data=json.dumps({"title": "To Kill a Mockingbird", "genre": "Fiction"}),
            content_type='application/json'
        )
        # Deleting the book
        response = self.app.delete('/books/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Book ID 1 and its reviews have been deleted.", response.get_data(as_text=True))

    def test_view_books_with_reviews(self):
        """Testing the GET /books endpoint."""
        # Adding a book and a review
        self.app.post(
            '/books',
            data=json.dumps({"title": "To Kill a Mockingbird", "genre": "Fiction"}),
            content_type='application/json'
        )
        self.app.post(
            '/books/1/reviews',
            data=json.dumps({"rating": 5, "note": "A masterpiece!"}),
            content_type='application/json'
        )
        # Viewing books with reviews
        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], "To Kill a Mockingbird")
        self.assertEqual(data[0]['genre'], "Fiction")

    def test_search_reviews(self):
        """Testing the GET /books/<int:book_id>/reviews endpoint."""
        # Adding a book and a review
        self.app.post(
            '/books',
            data=json.dumps({"title": "To Kill a Mockingbird", "genre": "Fiction"}),
            content_type='application/json'
        )
        self.app.post(
            '/books/1/reviews',
            data=json.dumps({"rating": 5, "note": "A masterpiece!"}),
            content_type='application/json'
        )
        # Searching reviews
        response = self.app.get('/books/1/reviews')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['title'], "To Kill a Mockingbird")
        self.assertEqual(data['genre'], "Fiction")
        self.assertEqual(len(data['reviews']), 1)
        self.assertEqual(data['reviews'][0]['note'], "A masterpiece!")

    def test_search_by_genre(self):
        """Testing the GET /books/genre endpoint."""
        # Adding books
        self.app.post(
            '/books',
            data=json.dumps({"title": "To Kill a Mockingbird", "genre": "Fiction"}),
            content_type='application/json'
        )
        self.app.post(
            '/books',
            data=json.dumps({"title": "The Great Gatsby", "genre": "Fiction"}),
            content_type='application/json'
        )
        # Searching by genre
        response = self.app.get('/books/genre?genre=Fiction')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], "To Kill a Mockingbird")
        self.assertEqual(data[1]['title'], "The Great Gatsby")

if __name__ == '__main__':
    unittest.main()
