# Author: Aditi Jha, November 4, 2024
# Implementing REST API for my movie tab for our review app.

from flask import Flask, jsonify, request
import movies
import books  # Importing both modules

app = Flask(__name__)

# Custom 404 Error Handler to Return JSON Response
@app.errorhandler(404)
def not_found(error):
    return jsonify({"title": "404 Not Found", "message": "The requested URL was not found on the server."}), 404

# Movies Endpoints
@app.route('/movies', methods=['POST'])
def add_movie():
    print("POST /movies endpoint hit")
    data = request.get_json()
    movie_name = data.get("name")
    if movie_name:
        result = movies.add_movie(movie_name)
        return jsonify(result), 201
    return jsonify({"error": "Movie name is required"}), 400

@app.route('/movies/<int:movie_id>/reviews', methods=['POST'])
def add_review(movie_id):
    data = request.get_json()
    rating = data.get("rating")
    note = data.get("note")
    if rating is not None and note:
        result = movies.add_review(movie_id, rating, note)
        return jsonify(result), 201 if "error" not in result else 404
    return jsonify({"error": "Rating and note are required"}), 400

@app.route('/movies/<int:movie_id>/reviews/<int:review_id>', methods=['PUT'])
def edit_review(movie_id, review_id):
    data = request.get_json()
    rating = data.get("rating")
    note = data.get("note")
    result = movies.edit_review(movie_id, review_id, rating, note)
    return jsonify(result)

@app.route('/movies/<int:movie_id>/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(movie_id, review_id):
    result = movies.delete_review(movie_id, review_id)
    return jsonify(result)

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    result = movies.delete_movie(movie_id)
    return jsonify(result)

@app.route('/movies', methods=['GET'])
def view_reviews():
    all_reviews = movies.load_data()["movies"]
    return jsonify(all_reviews)

@app.route('/movies/<int:movie_id>/reviews', methods=['GET'])
def search_reviews(movie_id):
    result = movies.search_reviews(movie_id)
    return jsonify(result), 200 if "error" not in result else 404

# Books Endpoints
@app.route('/books', methods=['GET'])
def get_books():
    data = books.load_data()
    return jsonify(data), 200

@app.route('/books/<int:book_id>', methods=['GET'])
def get_single_book(book_id):
    book = books.get_book(book_id)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

@app.route('/books', methods=['POST'])
def create_book():
    book_data = request.json
    title = book_data.get('title')
    if title:
        new_book = books.add_book(title)
        return jsonify({"message": "Book added successfully", "book": new_book}), 201
    return jsonify({"error": "Title is required"}), 400

@app.route('/books/<int:book_id>/reviews', methods=['POST'])
def create_book_review(book_id):
    review_data = request.json
    rating = review_data.get('rating')
    note = review_data.get('note')
    if rating is not None and note is not None:
        new_review = books.add_review(book_id, rating, note)
        if new_review:
            return jsonify({"message": "Review added successfully", "review": new_review}), 201
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"error": "Rating and note are required"}), 400

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_single_book(book_id):
    success = books.delete_book(book_id)
    if success:
        return jsonify({"message": f"Book ID {book_id} deleted"}), 200
    return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
