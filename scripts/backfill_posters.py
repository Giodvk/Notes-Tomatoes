import os
import sys
import time

from dotenv import load_dotenv
from pymongo import MongoClient
from backend.tmdb_service import fetch_poster_url

def backfill_movie_posters():
    """
    Finds movies in the database missing a 'poster_url' and fetches it from TMDb.
    This is an offline script, meant to be run manually.
    """
    # Load environment variables from .env in the project root
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path=dotenv_path)

    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
    COLLECTION_NAME = "Film_Rotten_Tomatoes" 

    if not all([MONGO_URI, DB_NAME]):
        print(" Error: MONGO_URI and DB_NAME must be set in your .env file.")
        sys.exit(1)

    print(" Starting poster backfill process...")
    client = None
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Query for movies where 'poster_url' is null, doesn't exist, or is an empty string
        query = {"poster_url": {"$in": [None, ""]}}
        movies_to_update = list(collection.find(query))
        
        total_movies = len(movies_to_update)
        if total_movies == 0:
            print("All movies already have a poster URL. Nothing to do.")
            return

        print(f"Found {total_movies} movies missing a poster. Starting fetch...")

        for i, movie in enumerate(movies_to_update):
            movie_title = movie.get("movie_title")
            movie_id = movie.get("_id")
            
            print(f"[{i+1}/{total_movies}] Fetching poster for: '{movie_title}'...")

            # Use your existing function to get the poster URL
            poster_url = fetch_poster_url(movie_title)

            if poster_url:
                # If a poster is found, update the document in the database
                collection.update_one(
                    {"_id": movie_id},
                    {"$set": {"poster_url": poster_url}}
                )
                print(f"    Success! Updated poster.")
            else:
                # If not found, you could set a specific value to avoid re-checking it
                # For now, we'll just log it.
                print(f"    Poster not found on TMDb for '{movie_title}'.")
            
            # --- CRITICAL: Lets Be a good API citizen! ---
            # Lets Wait for a fraction of a second between requests to not get blocked by TMDB
            time.sleep(0.25) # 4 requests per second

    except Exception as e:
        print(f" An error occurred: {e}")
    finally:
        if client:
            client.close()
            print("\nConnection closed. Process finished.")

if __name__ == "__main__":
    backfill_movie_posters()