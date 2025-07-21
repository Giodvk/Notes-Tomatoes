
import pymongo
from bson import ObjectId
from logging import getLogger
from bson.errors import InvalidId

logger = getLogger(__name__)


class OperatorFilm:

    def __init__(self, database: pymongo.database, name_collection):
        self.collection = database.get_collection(name_collection)

    def create_film(self, film_data: dict):
        self.collection.insert_one(film_data)
        logger.info(f"Inserted film {film_data['title']}")

    def delete_film(self, film_id: ObjectId):
        try:
            self.collection.delete_one({'_id': ObjectId(film_id)})
            logger.info(f"Deleted film {film_id}")
        except InvalidId:
            logger.info(f"Invalid id {film_id}")

    def get_film_by_id(self, film_id: ObjectId):
        return self.collection.find_one({'_id': ObjectId(film_id)})

    def get_film_by_title(self, film_title: str):
        return list(self.collection.find({'movie_title': film_title}))

    def get_film_by_title_async(self, film_initial: str):
        return list(self.collection.find({'movie_title': {'$regex': "^" + film_initial, "$options": "i"}},
                                         {'movie_title': 1}).limit(5))

    def get_film_by_genre(self, film_genre: str):
        return list(self.collection.aggregate(
            {
                '$in': [film_genre, '$genres']
            }
        ))

    def get_film_by_tomato_rating(self, rating:int):
        return list(self.collection.find({'tomato_rating': {'$gte': rating}}))

    def get_all_films(self):
        return list(self.collection.find())
