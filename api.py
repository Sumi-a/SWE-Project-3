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
@app.route('/books', methods=['GET'])
def get_books():
    data = books.get_all_books()
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

@app.route('/books/genre', methods=['GET'])
def get_books_by_genre():
    genre = request.args.get('genre', '')
    filtered_books = books.filter_books_by_genre(genre)
    if not filtered_books:
        return jsonify({"message": f"No books found in the '{genre}' genre."}), 404
    return jsonify(filtered_books), 200

# Removed the duplicate endpoint




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