# Core Backend Functioning of book tab of the review app
# Author: Kai Francis
# Date: Updated December 6, 2024

import sqlite3

DATABASE = 'books.db'

# Utility to get a database connection
import sqlite3

DATABASE = "books.db"  # Use in-memory database for testing

def get_connection():
    """Returns a database connection and initializes tables if necessary."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    # Initialize tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            rating INTEGER CHECK (rating BETWEEN 1 AND 5),
            note TEXT NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')
    connection.commit()
    return connection


# Adding a new book with genre
def add_book(book_title, genre):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO books (title, genre) VALUES (?, ?)"
    cursor.execute(query, (book_title, genre))
    connection.commit()
    book_id = cursor.lastrowid
    connection.close()
    return {"message": f"Book '{book_title}' added successfully.", "book": {"id": book_id, "title": book_title, "genre": genre}}

# Adding a review to a book
def add_review(book_id, rating, note):
    conn = get_connection()
    cursor = conn.cursor()
    query = 'INSERT INTO reviews (book_id, rating, note) VALUES (?, ?, ?)'
    cursor.execute(query, (book_id, rating, note))
    conn.commit()
    review_id = cursor.lastrowid
    conn.close()
    return {"message": f"Review added to book ID {book_id}.", "review_id": review_id}


# Editing a review
def edit_review(book_id, review_id, rating=None, note=None):
    connection = get_connection()
    cursor = connection.cursor()
    updates = []
    values = []

    if rating is not None:
        updates.append("rating = ?")
        values.append(rating)
    if note is not None:
        updates.append("note = ?")
        values.append(note)
    values.extend([book_id, review_id])

    query = f"UPDATE reviews SET {', '.join(updates)} WHERE book_id = ? AND id = ?"
    cursor.execute(query, tuple(values))
    connection.commit()
    connection.close()
    return {"message": f"Review ID {review_id} for book ID {book_id} updated."}

# Deleting a review
def delete_review(book_id, review_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = "DELETE FROM reviews WHERE book_id = ? AND id = ?"
    cursor.execute(query, (book_id, review_id))
    connection.commit()
    connection.close()
    return {"message": f"Review ID {review_id} deleted from book ID {book_id}."}

# Deleting a book
def delete_book(book_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = "DELETE FROM reviews WHERE book_id = ?"
    cursor.execute(query, (book_id,))
    delete_book_query = "DELETE FROM books WHERE id = ?"
    cursor.execute(delete_book_query, (book_id,))
    connection.commit()
    connection.close()
    return {"message": f"Book ID {book_id} and its reviews have been deleted."}

# Viewing all books
def view_books():
    connection = get_connection()
    cursor = connection.cursor()
    query = """
    SELECT b.id, b.title, b.genre, COUNT(r.id) as reviews_count
    FROM books b
    LEFT JOIN reviews r ON b.id = r.book_id
    GROUP BY b.id, b.title, b.genre
    """
    cursor.execute(query)
    books = [
        {"id": row[0], "title": row[1], "genre": row[2], "reviews_count": row[3], "reviews": []}
        for row in cursor.fetchall()
    ]
    connection.close()
    return books

def search_reviews(book_id):
    """Search for a book by ID and retrieve its reviews."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    # Fetch the book details
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    if not book:
        connection.close()
        return {"error": "Book not found."}
    
    # Fetch all reviews for the book
    cursor.execute('SELECT * FROM reviews WHERE book_id = ?', (book_id,))
    reviews = cursor.fetchall()
    connection.close()
    
    # Return the book and its reviews
    return {
        "id": book[0],
        "title": book[1],
        "genre": book[2],
        "reviews": [{"review_id": r[0], "rating": r[2], "note": r[3]} for r in reviews]
    }


def view_books_with_reviews():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    result = []
    for book in books:
        cursor.execute('SELECT * FROM reviews WHERE book_id = ?', (book[0],))
        reviews = cursor.fetchall()
        result.append({
            "id": book[0],
            "title": book[1],
            "genre": book[2],
            "reviews": [{"review_id": r[0], "rating": r[2], "note": r[3]} for r in reviews]
        })
    connection.close()
    return result


# Searching books by genre
def search_by_genre(genre):
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT id, title, genre FROM books WHERE LOWER(genre) LIKE ?"
    cursor.execute(query, (f"%{genre.lower()}%",))
    books = [
        {"id": row[0], "title": row[1], "genre": row[2]}
        for row in cursor.fetchall()
    ]
    connection.close()
    return books

def view_book_genres():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT genre FROM books')
    genres = [row[0] for row in cursor.fetchall()]
    connection.close()
    return genres

def view_top_books():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT book_id, AVG(rating) as avg_rating FROM reviews GROUP BY book_id ORDER BY avg_rating DESC LIMIT 3')
    top_books = cursor.fetchall()
    result = [{"book_id": row[0], "average_rating": row[1]} for row in top_books]
    connection.close()
    return result



