# backend/db.py
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

_MONGO_URI = os.getenv("MONGO_URI")
_DB_NAME   = os.getenv("DB_NAME")

_client = MongoClient(_MONGO_URI, server_api=ServerApi("1"))
_db     = _client[_DB_NAME]

def get_db():
    """Ritorna l'oggetto Database di PyMongo (singleton)."""
    return _db
