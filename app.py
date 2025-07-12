from bson import ObjectId
from flask import Flask, abort
from pymongo import MongoClient, ReadPreference
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from dotenv import load_dotenv
from flask import Flask, render_template
import os

from backend.movie_service import get_certified_fresh, get_most_review, get_longest, get_movie_by_id, get_movie_review

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

# ── HOME ──────────────────────────────────────────────────────────
@app.route("/")
def home():
    movies = get_certified_fresh(limit=15)
    recent = get_longest(limit=15)
    top = get_most_review(limit=15)
    return render_template("home.html", movies=movies, recent=recent, top=top)


@app.route('/film/<movie_id>')
def pagina_film(movie_id):
    movie = get_movie_by_id(movie_id)
    if not movie:
        return "Film non trovato", 404

    reviews = get_movie_review(movie_id)
    return render_template("paginaFilm.html", movie=movie, reviews=reviews)



if __name__ == "__main__":
    app.run(debug=True)
