from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_restful import Resource


def Order_setMongo(mongo):
    global m
    m = mongo
    m = m.db.orders

class Orders(Resource):
    def get(self):
        orders = m.find()
        resp = dumps(orders)
        return resp

class Order(Resource):
    def get (self, id):
        order = m.find_one({'_id': ObjectId(id)})
        resp = dumps(order)
        return resp
