from .db import get_db
from .tmdb_service import fetch_poster_url

_db = get_db()
_movies = _db["Film_Rotten_Tomatoes"]


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
    Restituisce i film con il punteggio tomatometer_count più alto.
    - Ordina in modo decrescente per tomatometer_count (numeri interi).
    - Esclude eventuali documenti privi di quel campo o con valore nullo.
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
