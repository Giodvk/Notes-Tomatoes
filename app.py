from flask import Flask, abort
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import Flask, render_template
import os

from backend.movie_service import get_certified_fresh, get_most_review, get_longest

# Carica variabili da .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

app = Flask(__name__)

# Connessione a MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# ── HOME ──────────────────────────────────────────────────────────
@app.route("/")
def home():
    movies = get_certified_fresh(limit=15)
    recent = get_longest(limit=15)
    top = get_most_review(limit=15)
    return render_template("home.html", movies=movies, recent=recent, top=top)



if __name__ == "__main__":
    app.run(debug=True)
