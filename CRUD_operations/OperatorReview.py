
import pymongo
from bson import ObjectId
from logging import getLogger
from bson.errors import InvalidId

logger = getLogger(__name__)

class OperatorReview:

    def __init__(self, database: pymongo.database, name_collection):
        self.table = database.get_collection(name_collection)

    def create_review(self, data: dict):
        self.table.insert_one(data)
        logger.info(f"Inserted record of review {data['publisher_name']}")

    def delete_review_by_id(self, review_id):
        try:
            self.table.delete_one({'_id': ObjectId(review_id)})
            logger.info("Deleted review {}".format(review_id))
        except InvalidId:
            logger.error("Invalid Object ID {}".format(review_id))

    def delete_review_by_film(self, link_film):
        self.table.delete_many({'rotten_tomatoes_film': link_film})
        logger.info("Deleted records for film {}".format(link_film))

    def get_review_by_id(self, review_id):
        return self.table.find_one({'_id': ObjectId(review_id)})

    def get_review_by_film(self, link_film):
        return list(self.table.find({'rotten_tomatoes_link': link_film}))

    def get_review_by_score(self, score):
        return list(self.table.find({'review_score': {'$lte': score}}))

    def get_review_by_rotten_score(self, rotten_score):
        return list(self.table.find({'review_type': rotten_score}))

    def get_review_by_critic(self, critic_name):
        return list(self.table.find({'critic_name': critic_name}))

    def get_all(self):
        return list(self.table.find())

    def update_review_by_id(self, review_id, new_description):
        try:
            result = self.table.update_one({'_id': ObjectId(review_id)},
                              {'$set': {'description': new_description}})
            logger.info(f"Updated {result.modified_count} records")
        except InvalidId:
            logger.error("Invalid Object ID {}".format(review_id))

    def update_review_publisher(self, old_publisher_name, new_review_publisher):
        result = self.table.update_many({'publisher_name': old_publisher_name},
                                        {'$set': {'publisher_name':new_review_publisher}})
        logger.info(f"Updated {result.modified_count} records with publisher_name {new_review_publisher}")

    def update_review_score_by_id(self, review_id, new_score):
        result = self.table.update_one({'_id': ObjectId(review_id)},
                                       {'$set': {'score': new_score}})
        logger.info(f"Updated {result.modified_count} records with score {new_score}")

    def join_reviews_by_score(self, rotten_score):
        """Prende il rotten score e ritorna la lista di tutti i
        titoli dei film che hanno quella valutazione"""
        return list(self.table.aggregate(
            [
                {
                    '$match': {
                        'review_type': rotten_score
                    }
                },
                {
                    '$lookup': {
                        'from': 'Film_Rotten_Tomatoes',
                        'localField': 'rotten_tomatoes_link',
                        'foreignField': 'rotten_tomatoes_link',
                        'as': 'film_infos'
                    }
                },
                {
                    '$project': {
                        'titolo': '$film_infos.movie_title',
                        'authors': '$film_infos.authors',
                        'directors': '$film_infos.directors'
                    }
                },
            ]))
