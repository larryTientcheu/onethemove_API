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
                upsert=True
            )

        return make_response("Updated", 200)

class OrderQueries():
    def addOrder(self, m, order):
        m.insert_one(order)
        return make_response("Order Added", 200)

    def updateOrder(self, m, id, status):
        m.update_one(
            {'_id': ObjectId(id)},
            {'$set': status},
            upsert=False)
        
        return make_response("Status Updated", 200)
        