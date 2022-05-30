from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_restful import Resource
from requests import request


def Order_setMongo(mongo):
    global m
    m = mongo
    m = m.db.orders

class Orders(Resource):
    def get(self):
        orders = m.find()
        resp = dumps(orders)
        return resp

    def post(self):
        _json = request.json
        _user = _json['user']
        _address = _json['address']
        _item = {'restaurant': _json['restaurant'], 
        'menu':{'drink': _json['drink'], 'meal': _json['meal']}}

class Order(Resource):
    def get (self, id):
        order = m.find_one({'_id': ObjectId(id)})
        resp = dumps(order)
        return resp
