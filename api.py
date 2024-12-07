# Author: Aditi Jha, November 4, 2024

from flask import Flask, jsonify, request
import movies
import books  
import tv_shows
app = Flask(__name__)

# Implementing REST API for my movie tab for our review app, author: Aditi, updated december 2, 2024

@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    name = data.get("name")
    genre = data.get("genre")
    if name and genre:
        return jsonify(movies.add_movie(name, genre)), 201
    return jsonify({"error": "Movie name and genre are required"}), 400

@app.route('/movies/<int:movie_id>/reviews', methods=['POST'])
def add_review(movie_id):
    data = request.get_json()
    rating = data.get("rating")
    note = data.get("note")
    if rating and note:
        return jsonify(movies.add_review(movie_id, rating, note)), 201
    return jsonify({"error": "Rating and note are required"}), 400

@app.route('/movies/<int:movie_id>/reviews/<int:review_id>', methods=['PUT'])
def edit_review(movie_id, review_id):
    data = request.get_json()
    rating = data.get("rating")
    note = data.get("note")
    return jsonify(movies.edit_review(movie_id, review_id, rating, note))

@app.route('/movies/<int:movie_id>/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(movie_id, review_id):
    return jsonify(movies.delete_review(movie_id, review_id))

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    return jsonify(movies.delete_movie(movie_id))

@app.route('/movies', methods=['GET'])
def view_reviews():
    return jsonify(movies.view_reviews())

@app.route('/movies/<int:movie_id>/reviews', methods=['GET'])
def search_reviews(movie_id):
    return jsonify(movies.search_reviews(movie_id))


@app.route('/movies/genre', methods=['GET'])
def search_by_genre():
    genre = request.args.get("genre")
    if not genre:
        return jsonify({"error": "Genre is required"}), 400
    try:
        result = movies.search_by_genre(genre)
        return jsonify(result)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while searching by genre."}), 500
    





# Books Endpoints
# View all books with reviews
@app.route('/books', methods=['GET'])
def get_books():
    try:
        data = books.view_books()  # Correct function from books.py
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_single_book(book_id):
    try:
        book = books.search_reviews(book_id)  # Retrieves book and its reviews
        if book:
            return jsonify(book), 200
        return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a new book
@app.route('/books', methods=['POST'])
def create_book():
    try:
        book_data = request.json
        title = book_data.get('title')
        genre = book_data.get('genre')
        if title and genre:
            result = books.add_book(title, genre)
            return jsonify(result), 201
        return jsonify({"error": "Title and Genre are required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a review to a book
@app.route('/books/<int:book_id>/reviews', methods=['POST'])
def create_book_review(book_id):
    try:
        review_data = request.json
        rating = review_data.get('rating')
        note = review_data.get('note')
        if rating is not None and note:
            result = books.add_review(book_id, rating, note)
            return jsonify(result), 201
        return jsonify({"error": "Rating and Note are required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Edit a review for a book
@app.route('/books/<int:book_id>/reviews/<int:review_id>', methods=['PUT'])
def edit_book_review(book_id, review_id):
    try:
        review_data = request.json
        rating = review_data.get('rating')
        note = review_data.get('note')
        result = books.edit_review(book_id, review_id, rating, note)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a review for a book
@app.route('/books/<int:book_id>/reviews/<int:review_id>', methods=['DELETE'])
def delete_book_review(book_id, review_id):
    try:
        result = books.delete_review(book_id, review_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a book and its reviews
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_single_book(book_id):
    try:
        result = books.delete_book(book_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Search books by genre
@app.route('/books/genre', methods=['GET'])
def get_books_by_genre():
    try:
        genre = request.args.get('genre', '').strip()
        if not genre:
            return jsonify({"error": "Genre is required"}), 400
        filtered_books = books.search_by_genre(genre)
        if not filtered_books:
            return jsonify({"message": f"No books found in the '{genre}' genre."}), 404
        return jsonify(filtered_books), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_with_reviews(book_id):
    result = books.search_reviews(book_id)
    return jsonify(result), 200


# Tv_shows Endpoint
#Mastewal 

@app.route('/tv_shows', methods=['POST'])
def add_tv_show():
    data = request.get_json()
    title = data.get("title")
    genre = data.get("genre")
    if title and genre:
        return jsonify(tv_shows.add_show(title, genre)), 201
    return jsonify({"error": "TV Show title and genre are required"}), 400

@app.route('/tv_shows/<int:tv_show_id>/reviews', methods=['POST'])
def add_tv_review(tv_show_id):
    data = request.get_json()
    rating = data.get("rating")
    note = data.get("note")
    if rating and note:
        return jsonify(tv_shows.add_review(tv_show_id, rating, note)), 201
    return jsonify({"error": "Rating and note are required"}), 400

@app.route('/tv_shows/<int:tv_show_id>/reviews/<int:review_id>', methods=['PUT'])
def edit_tv_review(tv_show_id, review_id):
    data = request.get_json()
    rating = data.get("rating")
    note = data.get("note")
    return jsonify(tv_shows.edit_review(tv_show_id, review_id, rating, note))

@app.route('/tv_shows/<int:tv_show_id>/reviews/<int:review_id>', methods=['DELETE'])
def delete_tv_review(tv_show_id, review_id):
    return jsonify(tv_shows.delete_review(tv_show_id, review_id))

@app.route('/tv_shows/<int:tv_show_id>', methods=['DELETE'])
def delete_tv_show(tv_show_id):
    return jsonify(tv_shows.delete_show(tv_show_id))

@app.route('/tv_shows', methods=['GET'])
def view_tv_reviews():
    return jsonify(tv_shows.view_reviews())

@app.route('/tv_shows/<int:tv_show_id>/reviews', methods=['GET'])
def search_tv_reviews(tv_show_id):
    return jsonify(tv_shows.search_reviews(tv_show_id))

@app.route('/tv_shows/genre', methods=['GET'])
def search_tv_by_genre():
    genre = request.args.get("genre")
    if not genre:
        return jsonify({"error": "Genre is required"}), 400
    try:
        result = tv_shows.search_by_genre(genre)
        return jsonify(result)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while searching by genre."}), 500


if __name__ == '__main__':
    app.run(debug=True)