import os
import sys
from pymongo import MongoClient, TEXT
from pymongo.errors import OperationFailure
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = "Film_Rotten_Tomatoes"
# scripts/manage_indexes.py

import os
import sys
from pymongo import MongoClient, TEXT
from pymongo.errors import OperationFailure
from dotenv import load_dotenv

# --- Path setup to import from other directories ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# --- Configuration ---
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = "Film_Rotten_Tomatoes"

def get_collection():
    """Helper function to connect and return the collection object."""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return client, db[COLLECTION_NAME]

def list_indexes():
    """Lists all indexes on the collection."""
    client, collection = get_collection()
    print(f"--- Indexes on {DB_NAME}.{COLLECTION_NAME} ---")
    try:
        for index in collection.list_indexes():
            print(index)
    finally:
        client.close()
    print("------------------------------------------")

def drop_index(index_name: str):
    """Drops a specific index by its name."""
    client, collection = get_collection()
    print(f"Attempting to drop index: '{index_name}'...")
    try:
        # The correct PyMongo method is drop_index
        collection.drop_index(index_name)
        print(f" Index '{index_name}' dropped successfully.")
    except OperationFailure as e:
        print(f" Error dropping index: {e}. It might not exist. Use 'list' to check.")
    finally:
        client.close()

def create_weighted_index():
    """Creates the new, improved weighted text index."""
    client, collection = get_collection()
    index_name = "movie_search_index"
    print(f"Attempting to create weighted text index '{index_name}'...")
    try:
        collection.create_index(
            [
                ('movie_title', TEXT)
            ],
            name=index_name
        )
        print(f" Weighted text index '{index_name}' created successfully.")
    except OperationFailure as e:
        print(f" Error creating index: {e}. It might already exist.")
    finally:
        client.close()

if __name__ == "__main__":
    if not all([MONGO_URI, DB_NAME]):
        print(" Error: MONGO_URI and DB_NAME must be set in your .env file.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("\nUsage: python scripts/manage_indexes.py [list|drop|create]")
        print("  list         - Shows all current indexes.")
        print("  drop <name>  - Drops the index with the given name.")
        print("  create       - Creates the new weighted search index.")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "list":
        list_indexes()
    elif command == "drop":
        if len(sys.argv) < 3:
            print(" Error: You must provide an index name to drop.")
            print("   Usage: python scripts/manage_indexes.py drop <index_name>")
        else:
            index_to_drop = sys.argv[2]
            drop_index(index_to_drop)
    elif command == "create":
        create_weighted_index()
    else:
        print(f" Unknown command: '{command}'")