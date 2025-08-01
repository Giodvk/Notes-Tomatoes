
from flask import Flask, abort, jsonify,render_template, request
from pymongo import MongoClient, ReadPreference
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from dotenv import load_dotenv
import os
from CRUD_operations.OperatorFilm import OperatorFilm
from backend.movie_service import get_certified_fresh, get_most_review, get_longest, get_movie_by_id, get_movie_review, \
    search_movies_by_text, insert_review, delete_review, update_review, get_rotten

# Carica variabili da .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

app = Flask(__name__)

# Connessione a MongoDB
client = MongoClient(MONGO_URI,
                     readPreference='secondaryPreferred')
db = client.get_database(
    DB_NAME,
    read_concern=ReadConcern("majority"),
    write_concern=WriteConcern(w=2, wtimeout=1000)
)

film_operator = OperatorFilm(db, "Film_Rotten_Tomatoes")
# ── HOME ──────────────────────────────────────────────────────────
@app.route("/")
def home():
    movies = get_certified_fresh(limit=15)
    recent = get_longest(limit=15)
    top = get_rotten(limit=15)
    return render_template("home.html", movies=movies, recent=recent, top=top)

@app.route("/info")
def info():
    return render_template("info.html")


@app.route('/film/<movie_id>')
def pagina_film(movie_id):
    movie = get_movie_by_id(movie_id)
    if not movie:
        return "Film non trovato", 404

    reviews = get_movie_review(movie_id)
    return render_template("paginaFilm.html", movie=movie, reviews=reviews)

@app.route("/inserisci_recensione/<movie_id>", methods=['POST'])
def inserisci_recensione(movie_id):
    insert_review(request.form, movie_id)
    movie = get_movie_by_id(movie_id)
    reviews = get_movie_review(movie_id)
    return render_template("paginaFilm.html", movie=movie, reviews=reviews)


@app.route("/delete_recensione", methods=['POST'])
def delete_recensione():
    review_id = request.form.get("review_id")
    delete_review(review_id)
    movie_id = request.form.get("movie_id")
    movie = get_movie_by_id(movie_id)
    reviews = get_movie_review(movie_id)
    return render_template("paginaFilm.html", movie=movie, reviews=reviews)

@app.route("/update_recensione/<movie_id>", methods=['POST'])
def update_recensione(movie_id):
    data = request.get_json()
    review_id = data["review_id"]
    new_desc = data["new_desc"]
    new_score = data["new_score"]
    update_review(review_id, new_desc, new_score)
    movie = get_movie_by_id(movie_id)
    reviews = get_movie_review(movie_id)
    return render_template("paginaFilm.html", movie=movie, reviews=reviews)



@app.route('/top-critic')
def top_critic():
    top_critics_movies = film_operator.get_top_critic_movies(limit=50)
    return render_template("topCritic.html", top_critics_movies=top_critics_movies)


@app.route('/api/search')
def api_search():
    # Get the search term from the URL query parameter (e.g., /api/search?q=inception)
    query = request.args.get('q', '').strip()

    # Avoid searching for very short or empty strings
    if len(query) < 2:
        return jsonify([])

    # Call your new, fast search function from movie_service
    movies = search_movies_by_text(query)

    # Return the results as a JSON array
    return jsonify(movies)

if __name__ == "__main__":
    app.run(debug=True)
