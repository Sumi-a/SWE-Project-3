import gradio as gr
import requests
import movies
import tv_shows
import books

# Base URL of the Flask API
BASE_URL = "http://127.0.0.1:5000"
 
# Functions to interact with the API


# First: Movie Tab functions, Aditi, Dec 2

# Adding a movie
def add_movie_frontend(movie_name, genre):
    # Aditi, dec 2, 2024
    if not movie_name.strip():
        return "❌ Error: Movie name cannot be empty!"
    if not genre.strip():
        return "❌ Error: Genre cannot be empty!"
    try:
        response = requests.post(f"{BASE_URL}/movies", json={"name": movie_name, "genre": genre})
        if response.status_code == 201:
            return response.json().get("message", "✅ Movie added successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Adding a review to a movie
def add_review_frontend(movie_id, rating, note):
    # Aditi, Dec 2, 2024
    if not movie_id.isdigit():
        return "❌ Error: Movie ID must be an integer!"
    if not (0 <= float(rating) <= 5):
        return "❌ Error: Rating must be between 0 and 5!"
    if not note.strip():
        return "❌ Error: Review note cannot be empty!"
    try:
        response = requests.post(
            f"{BASE_URL}/movies/{movie_id}/reviews",
            json={"rating": float(rating), "note": note},
        )
        if response.status_code == 201:
            return response.json().get("message", "✅ Review added successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Editing a review
def edit_review_frontend(movie_id, review_id, rating, note):
    # Aditi, Dec 2, 2024
    if not movie_id.isdigit() or not review_id.isdigit():
        return "❌ Error: Both Movie ID and Review ID must be integers!"
    try:
        response = requests.put(
            f"{BASE_URL}/movies/{movie_id}/reviews/{review_id}",
            json={"rating": float(rating), "note": note},
        )
        return response.json().get("message", "✅ Review updated successfully!")
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Deleting a review
def delete_review_frontend(movie_id, review_id):
    # Aditi, Dec 2, 2024
    if not movie_id.isdigit() or not review_id.isdigit():
        return "❌ Error: Both Movie ID and Review ID must be integers!"
    try:
        response = requests.delete(f"{BASE_URL}/movies/{movie_id}/reviews/{review_id}")
        return response.json().get("message", "✅ Review deleted successfully!")
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Deleting a movie
def delete_movie_frontend(movie_id):
    # Aditi, Dec 2, 2024
    if not movie_id.isdigit():
        return "❌ Error: Movie ID must be an integer!"
    try:
        response = requests.delete(f"{BASE_URL}/movies/{movie_id}")
        return response.json().get("message", "✅ Movie deleted successfully!")
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"


# Searching by genre
def search_by_genre_frontend(genre):
    # Aditi, Dec 2, 2024
    if not genre.strip():
        return "❌ Error: Genre cannot be empty!"
    try:
        response = requests.get(f"{BASE_URL}/movies/genre", params={"genre": genre})
        if response.status_code == 200:
            movies = response.json()
            if not movies:
                return f"🎥 No movies found under genre '{genre}'."
            output = [f"🎥 Movies under genre '{genre}':"]
            for movie in movies:
                output.append(f"Movie #{movie['id']}: {movie['name']}")
            return "\n".join(output)
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"


# Viewing all movies
def view_movies_frontend():
    # Aditi, Dec 2, 2024
    try:
        response = requests.get(f"{BASE_URL}/movies")
        if response.status_code == 200:
            movies = response.json()
            if not movies:
                return "🎥 No movies found. Add some to get started!"
            output = ["🎥 Movie List:"]
            for movie in movies:
                output.append(f"Movie #{movie['id']}: {movie['name']} (Genre: {movie['genre']})")
                if not movie["reviews"]:
                    output.append("   No reviews yet.")
                else:
                    for review in movie["reviews"]:
                        output.append(
                            f"   Review #{review['review_id']} | Rating: {review['rating']}/5 | {review['note']}"
                        )
            return "\n".join(output)
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Searching reviews by movie ID
def search_reviews_frontend(movie_id):
    # Aditi, Dec 2, 2024
    if not movie_id.isdigit():
        return "❌ Error: Movie ID must be an integer!"
    try:
        response = requests.get(f"{BASE_URL}/movies/{movie_id}/reviews")
        if response.status_code == 200:
            movie = response.json()
            output = [f"🎥 Movie: {movie['name']} (Genre: {movie['genre']})"]
            if not movie["reviews"]:
                output.append("   No reviews yet.")
            else:
                for review in movie["reviews"]:
                    output.append(
                        f"   Review #{review['review_id']} | Rating: {review['rating']}/5 | {review['note']}"
                    )
            return "\n".join(output)
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"
    




# tv_show 

def add_tv_show_frontend(title, genre):
    if not title.strip():
        return "❌ Error: TV Show title cannot be empty!"
    if not genre.strip():
        return "❌ Error: Genre cannot be empty!"
    try:
        response = requests.post(f"{BASE_URL}/tv_shows", json={"title": title, "genre": genre})
        if response.status_code == 201:
            return response.json().get("message", "✅ TV Show added successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Adding a review to a TV show
def add_tv_review_frontend(tv_show_id, rating, note):
    if not tv_show_id.isdigit():
        return "❌ Error: TV Show ID must be an integer!"
    if not (0 <= float(rating) <= 5):
        return "❌ Error: Rating must be between 0 and 5!"
    if not note.strip():
        return "❌ Error: Review note cannot be empty!"
    try:
        response = requests.post(
            f"{BASE_URL}/tv_shows/{tv_show_id}/reviews",
            json={"rating": float(rating), "note": note},
        )
        if response.status_code == 201:
            return response.json().get("message", "✅ Review added successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Editing a review
def edit_tv_review_frontend(tv_show_id, review_id, rating, note):
    if not tv_show_id.isdigit() or not review_id.isdigit():
        return "❌ Error: Both TV Show ID and Review ID must be integers!"
    try:
        response = requests.put(
            f"{BASE_URL}/tv_shows/{tv_show_id}/reviews/{review_id}",
            json={"rating": float(rating), "note": note},
        )
        return response.json().get("message", "✅ Review updated successfully!")
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Deleting a review
def delete_tv_review_frontend(tv_show_id, review_id):
    if not tv_show_id.isdigit() or not review_id.isdigit():
        return "❌ Error: Both TV Show ID and Review ID must be integers!"
    try:
        response = requests.delete(f"{BASE_URL}/tv_shows/{tv_show_id}/reviews/{review_id}")
        return response.json().get("message", "✅ Review deleted successfully!")
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Deleting a TV show
def delete_tv_show_frontend(tv_show_id):
    if not tv_show_id.isdigit():
        return "❌ Error: TV Show ID must be an integer!"
    try:
        response = requests.delete(f"{BASE_URL}/tv_shows/{tv_show_id}")
        return response.json().get("message", "✅ TV Show deleted successfully!")
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Searching by genre
def search_tv_by_genre_frontend(genre):
    if not genre.strip():
        return "❌ Error: Genre cannot be empty!"
    try:
        response = requests.get(f"{BASE_URL}/tv_shows/genre", params={"genre": genre})
        if response.status_code == 200:
            tv_shows = response.json()
            if not tv_shows:
                return f"📺 No TV Shows found under genre '{genre}'."
            output = [f"📺 TV Shows under genre '{genre}':"]
            for tv_show in tv_shows:
                output.append(f"TV Show #{tv_show['id']}: {tv_show['title']}")
            return "\n".join(output)
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Viewing all TV shows
def view_tv_shows_frontend():
    try:
        response = requests.get(f"{BASE_URL}/tv_shows")
        if response.status_code == 200:
            tv_shows = response.json()
            if not tv_shows:
                return "📺 No TV Shows found. Add some to get started!"
            output = ["📺 TV Show List:"]
            for tv_show in tv_shows:
                output.append(f"TV Show #{tv_show['id']}: {tv_show['title']} (Genre: {tv_show['genre']})")
                if not tv_show["reviews"]:
                    output.append("   No reviews yet.")
                else:
                    for review in tv_show["reviews"]:
                        output.append(
                            f"   Review #{review['review_id']} | Rating: {review['rating']}/5 | {review['note']}"
                        )
            return "\n".join(output)
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Searching reviews by TV show ID
def search_tv_reviews_frontend(tv_show_id):
    if not tv_show_id.isdigit():
        return "❌ Error: TV Show ID must be an integer!"
    try:
        response = requests.get(f"{BASE_URL}/tv_shows/{tv_show_id}/reviews")
        if response.status_code == 200:
            tv_show = response.json()
            output = [f"📺 TV Show: {tv_show['title']} (Genre: {tv_show['genre']})"]
            if not tv_show["reviews"]:
                output.append("   No reviews yet.")
            else:
                for review in tv_show["reviews"]:
                    output.append(
                        f"   Review #{review['review_id']} | Rating: {review['rating']}/5 | {review['note']}"
                    )
            return "\n".join(output)
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Adding a new book
def add_book(book_title, genre):
    if not book_title.strip():
        return "❌ Error: Book title cannot be empty!"
    if not genre.strip():
        return "❌ Error: Genre cannot be empty!"
    try:
        response = requests.post(f"{BASE_URL}/books", json={"title": book_title, "genre": genre})
        if response.status_code == 201:
            return response.json().get("message", "✅ Book added successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Adding a review to a book
def add_review(book_id, rating, note):
    if not book_id.isdigit():
        return "❌ Error: Book ID must be an integer!"
    if not (0 <= float(rating) <= 5):
        return "❌ Error: Rating must be between 0 and 5!"
    if not note.strip():
        return "❌ Error: Review note cannot be empty!"
    try:
        response = requests.post(
            f"{BASE_URL}/books/{book_id}/reviews",
            json={"rating": float(rating), "note": note},
        )
        if response.status_code == 201:
            return response.json().get("message", "✅ Review added successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Editing a review
def edit_review(book_id, review_id, rating=None, note=None):
    if not book_id.isdigit() or not review_id.isdigit():
        return "❌ Error: Both Book ID and Review ID must be integers!"
    payload = {}
    if rating is not None:
        if not (0 <= float(rating) <= 5):
            return "❌ Error: Rating must be between 0 and 5!"
        payload["rating"] = float(rating)
    if note:
        payload["note"] = note.strip()
    if not payload:
        return "❌ Error: No data provided for update!"
    try:
        response = requests.put(f"{BASE_URL}/books/{book_id}/reviews/{review_id}", json=payload)
        if response.status_code == 200:
            return response.json().get("message", "✅ Review updated successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Deleting a book
def delete_book(book_id):
    if not book_id.isdigit():
        return "❌ Error: Book ID must be an integer!"
    try:
        response = requests.delete(f"{BASE_URL}/books/{book_id}")
        if response.status_code == 200:
            return response.json().get("message", "✅ Book deleted successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Deleting a review
def delete_review(book_id, review_id):
    if not book_id.isdigit() or not review_id.isdigit():
        return "❌ Error: Both Book ID and Review ID must be integers!"
    try:
        response = requests.delete(f"{BASE_URL}/books/{book_id}/reviews/{review_id}")
        if response.status_code == 200:
            return response.json().get("message", "✅ Review deleted successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Searching books by genre
def search_books_by_genre(genre):
    if not genre.strip():
        return "❌ Error: Genre cannot be empty!"
    try:
        response = requests.get(f"{BASE_URL}/books/genre", params={"genre": genre})
        if response.status_code == 200:
            books = response.json()
            if not books:
                return f"📚 No books found under genre '{genre}'."
            output = [f"📚 Books under genre '{genre}':"]
            for book in books:
                output.append(f"Book #{book['id']}: {book['title']}")
            return "\n".join(output)
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Viewing all books
def view_books():
    try:
        response = requests.get(f"{BASE_URL}/books")
        if response.status_code == 200:
            books = response.json()
            if not books:
                return "📚 No books found. Add some to get started!"
            output = ["📚 Book List:"]
            for book in books:
                output.append(f"Book #{book['id']}: {book['title']} (Genre: {book['genre']})")
                if not book["reviews"]:
                    output.append("   No reviews yet.")
                else:
                    for review in book["reviews"]:
                        output.append(
                            f"   Review #{review['review_id']} | Rating: {review['rating']}/5 | {review['note']}"
                        )
            return "\n".join(output)
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

def search_book_reviews(book_id):
    if not book_id.strip().isdigit():
        return "❌ Error: Book ID must be a valid integer!"
    try:
        response = requests.get(f"{BASE_URL}/books/{book_id}/reviews")
        if response.status_code == 200:
            reviews = response.json()
            if not reviews:
                return f"📚 No reviews found for Book ID {book_id}."
            output = [f"📚 Reviews for Book ID {book_id}:"]
            for review in reviews:
                output.append(f"Review #{review['review_id']} | Rating: {review['rating']}/5 | {review['note']}")
            return "\n".join(output)
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}."
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Gradio Interface
# Rebecca Rogovich

# First: Movies tab:
with gr.Blocks() as demo:
    gr.Markdown("# 🎥 📺 📚Welcome to our Media Recommendation App!!")

    with gr.Tab("Movies"):
        gr.Markdown("# 🎥 Movies")
        with gr.Row():
            gr.Markdown("## Add a Movie")
            movie_name_input = gr.Textbox(label="Movie Name", placeholder="Enter movie name...")
            genre_input = gr.Textbox(label="Genre", placeholder="Enter movie genre...")
            movie_add_btn = gr.Button("Add Movie")
            movie_output = gr.Textbox(label="Status")
            movie_add_btn.click(add_movie_frontend, inputs=[movie_name_input, genre_input], outputs=movie_output)

        with gr.Row():
            del_movie_input = gr.Textbox(label="Delete Movie ID", placeholder="Enter movie ID...")
            del_movie_btn = gr.Button("Delete Movie")
            del_movie_output = gr.Textbox(label="Status")
            del_movie_btn.click(delete_movie_frontend, inputs=del_movie_input, outputs=del_movie_output)       

        with gr.Row():
            gr.Markdown("## Add a Review")
            movie_id_input = gr.Textbox(label="Movie ID", placeholder="Enter movie ID...")
            rating_input = gr.Slider(0, 5, step=0.5, label="Rating")
            review_note_input = gr.Textbox(label="Review Note", placeholder="Write your review...")
            review_add_btn = gr.Button("Add Review")
            review_output = gr.Textbox(label="Status")
            review_add_btn.click(
                add_review_frontend,
                inputs=[movie_id_input, rating_input, review_note_input],
                outputs=review_output,
            )
        with gr.Row():
            gr.Markdown("## Edit a Review")
            edit_movie_id_input = gr.Textbox(label="Movie ID", placeholder="Enter movie ID...")
            edit_review_id_input = gr.Textbox(label="Review ID", placeholder="Enter review ID...")
            edit_rating_input = gr.Slider(0, 5, step=0.5, label="New Rating")
            edit_review_note_input = gr.Textbox(label="New Review Note", placeholder="Update your review...")
            edit_review_btn = gr.Button("Edit Review")
            edit_review_output = gr.Textbox(label="Status")
            edit_review_btn.click(
                edit_review_frontend,
                inputs=[edit_movie_id_input, edit_review_id_input, edit_rating_input, edit_review_note_input],
                outputs=edit_review_output,
            )

        with gr.Row():
            gr.Markdown("## Delete a Review")
            del_movie_id_input = gr.Textbox(label="Movie ID", placeholder="Enter movie ID...")
            del_review_id_input = gr.Textbox(label="Review ID", placeholder="Enter review ID...")
            del_review_btn = gr.Button("Delete Review")
            del_review_output = gr.Textbox(label="Status")
            del_review_btn.click(
                delete_review_frontend,
                inputs=[del_movie_id_input, del_review_id_input],
                outputs=del_review_output,
            )

        with gr.Row():
            gr.Markdown("## Search by genre")
            genre_search_input = gr.Textbox(label="Genre", placeholder="Enter genre to search...")
            genre_search_btn = gr.Button("Search by Genre")
            genre_search_output = gr.Textbox(label="Movies by Genre", interactive=False)
            genre_search_btn.click(search_by_genre_frontend, inputs=genre_search_input, outputs=genre_search_output)

        with gr.Row():
            gr.Markdown("## Search Reviews by Movie ID")
            search_movie_id_input = gr.Textbox(label="Movie ID", placeholder="Enter movie ID...")
            search_reviews_btn = gr.Button("Search Reviews")
            search_reviews_output = gr.Textbox(label="Reviews", interactive=False)
            search_reviews_btn.click(search_reviews_frontend, inputs=search_movie_id_input, outputs=search_reviews_output)

        with gr.Row():
            gr.Markdown("## View Movies")
            view_movies_btn = gr.Button("View All Movies")
            movies_display = gr.Textbox(label="Movie List", interactive=False)
            view_movies_btn.click(view_movies_frontend, inputs=[], outputs=movies_display)

#TV Shows Tab

    with gr.Tab("TV Shows"):
        gr.Markdown("## 📺 TV Shows ")
        
        with gr.Row():
            gr.Markdown("## Add a TV Show")
            tv_show_title_input = gr.Textbox(label="TV Show Title", placeholder="Enter TV show title...")
            tv_genre_input = gr.Textbox(label="Genre", placeholder="Enter TV show genre...")
            tv_add_btn = gr.Button("Add TV Show")
            tv_output = gr.Textbox(label="Status")
            # Ensure this line is within the correct Gradio context
            tv_add_btn.click(add_tv_show_frontend, inputs=[tv_show_title_input, tv_genre_input], outputs=tv_output)

        with gr.Row():
            del_tv_show_input = gr.Textbox(label="Delete TV Show ID", placeholder="Enter TV show ID...")
            del_tv_show_btn = gr.Button("Delete TV Show")
            del_tv_show_output = gr.Textbox(label="Status")
            del_tv_show_btn.click(delete_tv_show_frontend, inputs=del_tv_show_input, outputs=del_tv_show_output)

        with gr.Row():
            gr.Markdown("## Add a Review")
            tv_show_id_input = gr.Textbox(label="TV Show ID", placeholder="Enter TV show ID...")
            tv_rating_input = gr.Slider(0, 5, step=0.5, label="Rating")
            tv_review_note_input = gr.Textbox(label="Review Note", placeholder="Write your review...")
            tv_review_add_btn = gr.Button("Add Review")
            tv_review_output = gr.Textbox(label="Status")
            tv_review_add_btn.click(
                add_tv_review_frontend,
                inputs=[tv_show_id_input, tv_rating_input, tv_review_note_input],
                outputs=tv_review_output,
            )

        with gr.Row():
            gr.Markdown("## Edit a Review")
            edit_tv_show_id_input = gr.Textbox(label="TV Show ID", placeholder="Enter TV show ID...")
            edit_tv_review_id_input = gr.Textbox(label="Review ID", placeholder="Enter review ID...")
            edit_tv_rating_input = gr.Slider(0, 5, step=0.5, label="New Rating")
            edit_tv_review_note_input = gr.Textbox(label="New Review Note", placeholder="Update your review...")
            edit_tv_review_btn = gr.Button("Edit Review")
            edit_tv_review_output = gr.Textbox(label="Status")
            edit_tv_review_btn.click(
                edit_tv_review_frontend,
                inputs=[edit_tv_show_id_input, edit_tv_review_id_input, edit_tv_rating_input, edit_tv_review_note_input],
                outputs=edit_tv_review_output,
            )


        with gr.Row():
            gr.Markdown("## Delete a Review")
            del_tv_show_id_input = gr.Textbox(label="TV Show ID", placeholder="Enter TV show ID...")
            del_tv_review_id_input = gr.Textbox(label="Review ID", placeholder="Enter review ID...")
            del_tv_review_btn = gr.Button("Delete Review")
            del_tv_review_output = gr.Textbox(label="Status")
            del_tv_review_btn.click(
                delete_tv_review_frontend,
                inputs=[del_tv_show_id_input, del_tv_review_id_input],
                outputs=del_tv_review_output,
            )

        with gr.Row():
            gr.Markdown("## Search by genre")
            tv_genre_search_input = gr.Textbox(label="Genre", placeholder="Enter genre to search...")
            tv_genre_search_btn = gr.Button("Search by Genre")
            tv_genre_search_output = gr.Textbox(label="TV Shows by Genre", interactive=False)
            tv_genre_search_btn.click(search_tv_by_genre_frontend, inputs=tv_genre_search_input, outputs=tv_genre_search_output)

        with gr.Row():
            gr.Markdown("## Search Reviews by TV Show ID")
            search_tv_show_id_input = gr.Textbox(label="TV Show ID", placeholder="Enter TV show ID...")
            search_tv_reviews_btn = gr.Button("Search Reviews")
            search_tv_reviews_output = gr.Textbox(label="Reviews", interactive=False)
            search_tv_reviews_btn.click(search_tv_reviews_frontend, inputs=search_tv_show_id_input, outputs=search_tv_reviews_output)

        with gr.Row():
            gr.Markdown("## View TV Shows")
            view_tv_shows_btn = gr.Button("View All TV Shows")
            tv_shows_display = gr.Textbox(label="TV Show List", interactive=False)
            view_tv_shows_btn.click(view_tv_shows_frontend, inputs=[], outputs=tv_shows_display)


# Books Tab
    with gr.Tab("Books"):
        gr.Markdown("## 📚 Books")

        with gr.Row():
            gr.Markdown("## Add a Book")
            book_title_input = gr.Textbox(label="Book Title", placeholder="Enter book title...")
            book_genre_input = gr.Textbox(label="Genre", placeholder="Enter book genre...")
            book_add_btn = gr.Button("Add Book")
            book_output = gr.Textbox(label="Status")
            book_add_btn.click(add_book, inputs=[book_title_input, book_genre_input], outputs=book_output)

        with gr.Row():
            del_book_input = gr.Textbox(label="Delete Book ID", placeholder="Enter book ID...")
            del_book_btn = gr.Button("Delete Book")
            del_book_output = gr.Textbox(label="Status")
            del_book_btn.click(delete_book, inputs=del_book_input, outputs=del_book_output)
        
        with gr.Row():
            gr.Markdown("## Add a Review")
            book_id_input = gr.Textbox(label="Book ID", placeholder="Enter book ID...")
            rating_input = gr.Slider(0, 5, step=0.5, label="Rating")
            review_note_input = gr.Textbox(label="Review Note", placeholder="Write your review...")
            review_add_btn = gr.Button("Add Review")
            review_output = gr.Textbox(label="Status")
            review_add_btn.click(
                add_review,
                inputs=[book_id_input, rating_input, review_note_input],
                outputs=review_output,
            )

        with gr.Row():
            gr.Markdown("## Edit a Review")
            edit_book_id_input = gr.Textbox(label="Book ID", placeholder="Enter book ID...")
            edit_review_id_input = gr.Textbox(label="Review ID", placeholder="Enter review ID...")
            edit_rating_input = gr.Slider(0, 5, step=0.5, label="New Rating")
            edit_review_note_input = gr.Textbox(label="New Review Note", placeholder="Update your review...")
            edit_review_btn = gr.Button("Edit Review")
            edit_review_output = gr.Textbox(label="Status")
            edit_review_btn.click(
                edit_review,
                inputs=[edit_book_id_input, edit_review_id_input, edit_rating_input, edit_review_note_input],
                outputs=edit_review_output,
            )

        with gr.Row():
            gr.Markdown("## Delete a Review")
            del_book_id_input = gr.Textbox(label="Book ID", placeholder="Enter book ID...")
            del_review_id_input = gr.Textbox(label="Review ID", placeholder="Enter review ID...")
            del_review_btn = gr.Button("Delete Review")
            del_review_output = gr.Textbox(label="Status")
            del_review_btn.click(
                delete_review,
                inputs=[del_book_id_input, del_review_id_input],
                outputs=del_review_output,
            )

        with gr.Row():
            gr.Markdown("## Search by genre")
            book_genre_search_input = gr.Textbox(label="Genre", placeholder="Enter genre to search...")
            book_genre_search_btn = gr.Button("Search by Genre")
            book_genre_search_output = gr.Textbox(label="Books by Genre", interactive=False)
            book_genre_search_btn.click(search_books_by_genre, inputs=book_genre_search_input, outputs=book_genre_search_output)

        with gr.Row():
            gr.Markdown("## Search Reviews by Book ID")
            search_book_id_input = gr.Textbox(label="Book ID", placeholder="Enter book ID...")
            search_reviews_btn = gr.Button("Search Reviews")
            search_reviews_output = gr.Textbox(label="Reviews", interactive=False)
            search_reviews_btn.click(search_book_reviews, inputs=search_book_id_input, outputs=search_reviews_output)

        with gr.Row():
            gr.Markdown("## View Books")
            view_books_btn = gr.Button("View All Books")
            books_display = gr.Textbox(label="Book List", interactive=False)
            view_books_btn.click(view_books, inputs=[], outputs=books_display)






if __name__ == "__main__":
    demo.launch( debug=True)



