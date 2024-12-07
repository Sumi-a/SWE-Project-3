import unittest
import sqlite3
import books

class TestBooks(unittest.TestCase):

    def setUp(self):
        """Setting up a shared in-memory database before each test."""
        self.conn = sqlite3.connect(":memory:")  # Single in-memory database
        self.cursor = self.conn.cursor()

        # Creating tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                rating INTEGER CHECK (rating BETWEEN 1 AND 5),
                note TEXT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books (id)
            )
        ''')
        self.conn.commit()

        # Override books.get_connection to return the shared connection
        books.get_connection = lambda: self.conn

    def tearDown(self):
        """Closing the shared connection after each test."""
        self.conn.close()

    def test_add_book(self):
        """Testing adding a book to the database."""
        response = books.add_book("1984", "Dystopian")
        self.cursor.execute('SELECT * FROM books WHERE title = ?', ("1984",))
        book = self.cursor.fetchone()
        self.assertIsNotNone(book)
        self.assertEqual(book[1], "1984")
        self.assertEqual(book[2], "Dystopian")
        self.assertEqual(response["message"], "Book '1984' added successfully.")

    def test_add_review(self):
        """Testing adding a review to a book."""
        books.add_book("1984", "Dystopian")
        response = books.add_review(1, 5, "Excellent book!")
        self.cursor.execute('SELECT * FROM reviews WHERE book_id = ?', (1,))
        review = self.cursor.fetchone()
        self.assertIsNotNone(review)
        self.assertEqual(review[2], 5)
        self.assertEqual(review[3], "Excellent book!")
        self.assertEqual(response["message"], "Review added to book ID 1.")

    def test_edit_review(self):
        """Testing editing a review."""
        books.add_book("1984", "Dystopian")
        books.add_review(1, 4, "Good book")
        response = books.edit_review(1, 1, rating=5, note="Amazing book!")
        self.cursor.execute('SELECT * FROM reviews WHERE id = 1')
        review = self.cursor.fetchone()
        self.assertIsNotNone(review)
        self.assertEqual(review[2], 5)
        self.assertEqual(review[3], "Amazing book!")
        self.assertEqual(response["message"], "Review ID 1 for book ID 1 updated.")

    def test_delete_review(self):
        """Testing deleting a review."""
        books.add_book("1984", "Dystopian")
        books.add_review(1, 5, "Excellent book!")
        response = books.delete_review(1, 1)
        self.cursor.execute('SELECT * FROM reviews WHERE id = 1')
        review = self.cursor.fetchone()
        self.assertIsNone(review)
        self.assertEqual(response["message"], "Review ID 1 deleted from book ID 1.")

    def test_delete_book(self):
        """Testing deleting a book and its reviews."""
        books.add_book("1984", "Dystopian")
        books.add_review(1, 5, "Excellent book!")
        response = books.delete_book(1)
        self.cursor.execute('SELECT * FROM books WHERE id = 1')
        book = self.cursor.fetchone()
        self.cursor.execute('SELECT * FROM reviews WHERE book_id = 1')
        review = self.cursor.fetchone()
        self.assertIsNone(book)
        self.assertIsNone(review)
        self.assertEqual(response["message"], "Book ID 1 and its reviews have been deleted.")

    def test_view_books_with_reviews(self):
        """Testing viewing all books with their reviews."""
        books.add_book("1984", "Dystopian")
        books.add_review(1, 5, "Excellent book!")
        response = books.view_books_with_reviews()
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]["title"], "1984")
        self.assertEqual(response[0]["genre"], "Dystopian")
        self.assertEqual(len(response[0]["reviews"]), 1)
        self.assertEqual(response[0]["reviews"][0]["note"], "Excellent book!")

    def test_view_book_genres(self):
        """Testing viewing distinct book genres."""
        books.add_book("1984", "Dystopian")
        books.add_book("Brave New World", "Dystopian")
        books.add_book("To Kill a Mockingbird", "Classic")
        genres = books.view_book_genres()
        self.assertIn("Dystopian", genres)
        self.assertIn("Classic", genres)
        self.assertEqual(len(genres), 2)

    def test_view_top_books(self):
        """Testing viewing top 3 books by average rating."""
        books.add_book("1984", "Dystopian")
        books.add_book("Brave New World", "Dystopian")
        books.add_book("To Kill a Mockingbird", "Classic")
        books.add_review(1, 5, "Amazing")
        books.add_review(2, 4, "Good")
        books.add_review(3, 3, "Okay")
        top_books = books.view_top_books()
        self.assertEqual(len(top_books), 3)
        self.assertEqual(top_books[0]["book_id"], 1)
        self.assertGreater(top_books[0]["average_rating"], top_books[2]["average_rating"])

    def test_search_by_genre(self):
        """Testing searching for books by genre."""
        books.add_book("1984", "Dystopian")
        books.add_book("Brave New World", "Dystopian")
        response = books.search_by_genre("Dystopian")
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["title"], "1984")
        self.assertEqual(response[1]["title"], "Brave New World")

if __name__ == "__main__":
    unittest.main()

