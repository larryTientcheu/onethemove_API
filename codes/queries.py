from flask import jsonify, make_response
from bson.objectid import ObjectId

class RestaurantQueries():
    def addRestaurant(self, m, restaurant):
        m.insert_one(restaurant)
        return make_response("Added", 200)


    def updateRestaurant(self, m, id, operation, arrayFilters):
        m.update_one(
                {'_id': ObjectId(id)},
                update = operation, 
                array_filters = arrayFilters,
                upsert=False
            )

        return make_response("Updated", 200)