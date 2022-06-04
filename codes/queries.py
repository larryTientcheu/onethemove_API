from flask import jsonify, make_response
from bson.objectid import ObjectId

def updateRestaurant(m, id, operation, arrayFilters):
    m.update_one(
            {'_id': ObjectId(id)},
            update = operation, 
            array_filters = arrayFilters,
            upsert=False
        )

    return make_response("Updated", 200)