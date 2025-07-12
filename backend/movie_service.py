from .db import get_db
from .tmdb_service import fetch_poster_url, fetch_trailer_url
from bson import ObjectId

_db = get_db()
_movies = _db["Film_Rotten_Tomatoes"]
_reviews = _db["Review_Rotten_Tomatoes"]


def _ensure_poster(movie: dict) -> str | None:
    if poster := movie.get("poster_url"):
        print(f"Poster già presente per {movie['movie_title']}")
        return poster

    print(f"Chiamo TMDb per {movie['movie_title']}")
    poster = fetch_poster_url(movie["movie_title"])
    if poster:
        print(f"Trovato poster per {movie['movie_title']}: {poster}")
        _movies.update_one({"_id": movie["_id"]}, {"$set": {"poster_url": poster}})
    else:
        print(f"Nessun poster trovato per {movie['movie_title']}")
    return poster


def _ensure_trailer(movie: dict) -> str | None:
    if trailer := movie.get("trailer_url"):
        print(f"Trailer già presente per {movie['movie_title']}")
        return trailer

    print(f"Chiamo TMDb per trailer di {movie['movie_title']}")
    trailer = fetch_trailer_url(movie["movie_title"])
    if trailer:
        print(f"Trovato trailer per {movie['movie_title']}: {trailer}")
        _movies.update_one({"_id": movie["_id"]}, {"$set": {"trailer_url": trailer}})
    else:
        print(f"Nessun trailer trovato per {movie['movie_title']}")
    return trailer


def get_certified_fresh(limit=15):
    cur = (
        _movies.find(
            {"tomatometer_status": "Certified-Fresh"},
            {"movie_title": 1, "tomatometer_rating": 1, "poster_url": 1}
        )
        .sort("tomatometer_rating", -1)
        .limit(limit)
    )

    movies = []
    for m in cur:
        m["poster_url"] = _ensure_poster(m)
        movies.append(m)
    return movies


def get_longest(limit=15):
    cur = (
        _movies.find(
            {},  # nessun filtro, prendi tutti i film
            {"movie_title": 1, "original_release_date": 1, "tomatometer_rating": 1, "poster_url": 1}
        )
        .sort("runtime", -1)  # ordine decrescente per data
        .limit(limit)
    )

    movies = []
    for m in cur:
        m["poster_url"] = _ensure_poster(m)
        movies.append(m)
    return movies


def get_most_review(limit=15):
    """
    Restituisce i film con piu reviews.
    - Ordina in modo decrescente per numero di reviews.
    """
    cur = (
        _movies.find(
            { "tomatometer_count": { "$exists": True, "$ne": None } },
            { "movie_title": 1, "tomatometer_count": 1, "tomatometer_rating": 1, "poster_url": 1 }
        )
        .sort("tomatometer_count", -1)   # dal rating più alto in giù
        .limit(limit)
    )

    movies = []
    for m in cur:
        m["poster_url"] = _ensure_poster(m)   # recupera / cache poster se mancante
        movies.append(m)
    return movies

def get_movie_review(movie_id):
    try:
        movie_oid = ObjectId(movie_id)
    except Exception as e:
        print(f"ID non valido: {movie_id} – {e}")
        return []

    # Recupera il film
    movie = _movies.find_one({ "_id": movie_oid })
    if not movie or "rotten_tomatoes_link" not in movie:
        print("Film non trovato o campo 'rotten_tomatoes_link' mancante.")
        return []

    rt_link = movie["rotten_tomatoes_link"]

    # Recupera tutte le recensioni con lo stesso rotten_tomatoes_link
    reviews = list(_reviews.find(
        {"rotten_tomatoes_link": rt_link},
        {"critic_name": 1, "review_content": 1, "top_critic": 1, "publisher_name": 1, "review_date": 1, "review_score": 1, "_id": 0}
    ))

    return reviews


def get_movie_by_id(movie_id):
    try:
        movie_oid = ObjectId(movie_id)
    except Exception as e:
        print(f"ID non valido: {movie_id} – {e}")
        return None

    movie = _movies.find_one({"_id": movie_oid})
    if not movie:
        return None

    movie["poster_url"] = _ensure_poster(movie)
    movie["trailer_url"] = _ensure_trailer(movie)

    return movie