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



def fetch_trailer_url(title: str) -> str | None:
    """
    Cerca un film per titolo su TMDb e restituisce il link YouTube del trailer,
    oppure None se non disponibile.
    """
    if not _API_KEY or not title:
        return None

    # Step 1: cerca l'ID del film
    search_url = "https://api.themoviedb.org/3/search/movie"
    search_params = {"api_key": _API_KEY, "query": title}

    try:
        search_resp = requests.get(search_url, params=search_params, timeout=5)
        search_resp.raise_for_status()
        search_data = search_resp.json()

        if not search_data.get("results"):
            print(f"TMDb: Nessun risultato per '{title}'")
            return None

        movie_id = search_data["results"][0]["id"]

        # Step 2: ottieni i video associati al film
        video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"
        video_params = {"api_key": _API_KEY}
        video_resp = requests.get(video_url, params=video_params, timeout=5)
        video_resp.raise_for_status()
        video_data = video_resp.json()

        for video in video_data.get("results", []):
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                return f"https://www.youtube.com/watch?v={video['key']}"

        print(f"TMDb: Nessun trailer YouTube trovato per '{title}'")

    except Exception as exc:
        print("Errore TMDb (trailer):", exc)

    return None
