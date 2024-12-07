# Core Backend Functioning of book tab of the review app
# Author: Kai Francis
# Date: Updated December 6, 2024

import sqlite3

# Utility to get a database connection
def get_connection():
    return sqlite3.connect("books.db")

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
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO reviews (book_id, rating, note) VALUES (?, ?, ?)"
    cursor.execute(query, (book_id, rating, note))
    # Optionally update the reviews_count in books
    update_query = "UPDATE books SET reviews_count = reviews_count + 1 WHERE id = ?"
    cursor.execute(update_query, (book_id,))
    connection.commit()
    review_id = cursor.lastrowid
    connection.close()
    return {"message": f"Review added to book ID {book_id}.", "review": {"review_id": review_id, "rating": rating, "note": note}}

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
    query = "SELECT id, title, genre, reviews_count FROM books"
    cursor.execute(query)
    books = [
        {"id": row[0], "title": row[1], "genre": row[2], "reviews_count": row[3]}
        for row in cursor.fetchall()
    ]
    connection.close()
    return books

# Searching books by genre
def filter_books_by_genre(genre):
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

# Run initialization when the script is executed
def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            reviews_count INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            note TEXT NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    """)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()

