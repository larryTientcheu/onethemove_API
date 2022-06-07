from flask import jsonify, make_response
from bson.objectid import ObjectId


class AuthQueries():
    def registerUser(self, m, user):
        m.insert_one(user)
        return make_response("Registered", 201)

    def registerRestaurant(self, m, restaurant):
        m.insert_one(restaurant)
        return make_response("Created", 201)


class UserQueries():
    def updateUser(self, m, id, user):
        m.update_one(
            {'_id': ObjectId(id)},
            {'$set': user}, upsert= False
        )
        return make_response("Updated", 200)


class RestaurantQueries():
   
    def updateRestaurant(self, m, id, operation, arrayFilters):
        m.update_one(
                {'_id': ObjectId(id)},
                update = operation, 
                array_filters = arrayFilters,
                upsert=True
            )

        return make_response("Updated", 200)

    def updateRestaurantCredentials(self, m, id, credential):
        m.update_one(
                {'_id': ObjectId(id)},
                {'$set': credential},
                upsert = False
        )
        return make_response("Updated", 200)

class OrderQueries():
    def addOrder(self, m, order):
        m.insert_one(order)
        return make_response("Created", 200)

    def updateOrder(self, m, id, status):
        m.update_one(
            {'_id': ObjectId(id)},
            {'$set': status, "$currentDate": {"lastModified": True}},
            upsert=False)
        
        return make_response("Status Updated", 200)
        