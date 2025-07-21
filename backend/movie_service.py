import re
from datetime import datetime
from flask import url_for
from CRUD_operations.OperatorReview import OperatorReview
from .db import get_db
from .tmdb_service import fetch_poster_url, fetch_trailer_url
from bson import ObjectId
from CRUD_operations.OperatorFilm import OperatorFilm

_db = get_db()
_movies = _db["Film_Rotten_Tomatoes"]
_reviews = _db["Review_Rotten_Tomatoes"]
op_film = OperatorFilm(_db, "Film_Rotten_Tomatoes")


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
        print(f"Nessun poster trovato per {movie['movie_title']}, uso immagine di fallback")
        fallback_poster = url_for('static', filename='img/no_available.jpg')
        _movies.update_one({"_id": movie["_id"]}, {"$set": {"poster_url": fallback_poster}})
        return fallback_poster
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
        {"critic_name": 1, "review_content": 1, "top_critic": 1, "publisher_name": 1, "review_date": 1, "review_score": 1, "_id": 1}
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


def search_movies_by_text(query_text: str, limit: int = 10):
    if not query_text:
        return []

    try:
        escaped_query = re.escape(query_text)
        pipeline = [
            # STAGE 1: Match ANY document that either starts with the text OR is a text-search match.
            {
                '$match': {
                    '$or': [
                        {'movie_title': {'$regex': f'^{escaped_query}', '$options': 'i'}},
                        {'$text': {'$search': query_text}}
                    ]
                }
            },
            {
                '$addFields': {
                    'text_score': {'$meta': 'textScore'},
                    'prefix_boost': {
                        '$cond': {
                            'if': {'$regexMatch': {'input': '$movie_title', 'regex': f'^{escaped_query}', 'options': 'i'}},
                            'then': 100,
                            'else': 0
                        }
                    }
                }
            },
            {
                '$addFields': {
                    'total_score': {'$add': ['$text_score', '$prefix_boost']}
                }
            },
            {'$sort': {'total_score': -1}},
            {'$limit': limit},
            {'$project': {'movie_title': 1, 'poster_url': 1, 'original_release_date': 1, '_id': 1, 'total_score': 1}}
        ]
        
 
        # This abandons text search for the dropdown, which is often the right call.
        escaped_query = re.escape(query_text)
        
        # Find movies where the title starts with the query
        prefix_cursor = _movies.find(
            {'movie_title': {'$regex': f'^{escaped_query}', '$options': 'i'}},
            # Project the same fields
            {'movie_title': 1, 'poster_url': 1, 'original_release_date': 1}
        ).limit(limit)

        results = []
        for movie in prefix_cursor:
            movie['_id'] = str(movie['_id'])
            results.append(movie)

        return results

    except Exception as e:
        print(f"Database regex search error: {e}")
        return []


def insert_review(data_review, movie_id):
    review_dict = {}
    operatorReview = OperatorReview(_db, "Review_Rotten_Tomatoes")
    movie = op_film.get_film_by_id(movie_id)
    review_dict['rotten_tomatoes_link'] = movie['rotten_tomatoes_link']
    review_dict['critic_name'] = data_review.get('critic_name')
    review_dict['publisher_name'] = data_review.get('publisher_name')
    review_dict['review_score'] = data_review.get('review_score') + "/5"
    review_dict['top_critic'] = True if data_review.get('top_critic') else False
    review_dict['review_date'] = datetime.today()
    review_dict['review_content'] = data_review.get('review_content')
    operatorReview.create_review(review_dict)


def delete_review(review_id):
    operatorReview = OperatorReview(_db, "Review_Rotten_Tomatoes")
    operatorReview.delete_review_by_id(review_id)
