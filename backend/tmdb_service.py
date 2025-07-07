# backend/tmdb_service.py
import os, requests
from dotenv import load_dotenv

load_dotenv()
_API_KEY   = os.getenv("TMDB_API_KEY")
_BASE_IMG  = "https://image.tmdb.org/t/p/w342"   # larghezza 342 px

def fetch_poster_url(title: str) -> str | None:
    """
    Cerca un film per titolo e restituisce l'URL del poster.
    Ritorna None se non trovato o in caso di errore/chiave mancante.
    """
    if not _API_KEY or not title:
        return None

    search_url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": _API_KEY, "query": title}

    try:
        resp = requests.get(search_url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return f"{_BASE_IMG}{poster_path}"
    except Exception as exc:
        print("TMDb error:", exc)

    return None
