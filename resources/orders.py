from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_restful import Resource, abort
from flask import make_response
from flask.globals import request
from datetime import datetime
from codes.functions import Functions
from codes.dbfunc import OrderFunctions
from codes.queries import OrderQueries

func = Functions()
oFunc = OrderFunctions()
oQueries = OrderQueries()

def Order_setMongo(mongo):
    global m
    m = mongo
    m = m.db.orders

class Orders(Resource):
    def get(self):
        orders = m.find()
        resp = dumps(orders)
        return make_response(resp, 200)

    def post(self):
        _json = request.json
        order = oFunc.formatAddOrder(_json)
        resp = oQueries.addOrder(order)
        
        if resp.status != 200:
            message = 'Error while adding an order'
            abort(400, message=message)
        return resp

def formatUpdateOrder(_json):
    _status = _json['status']
    order = {'status': _status}
    if _status == 'delivered':
        _date_fulfilled = datetime.today()
        order = {'status': _status, 'date_fulfilled': _date_fulfilled}
    return order

class Order(Resource):
    def get (self, id):
        order = m.find_one({'_id': ObjectId(id)})
        func.abort_if_not_exist(order)
        resp = dumps(order)
        return make_response(resp, 200)

    def put(self, id):
        _json = request.json
        status = formatUpdateOrder(_json)
        order = m.find_one({'_id': ObjectId(id)})
        if 'date_fulfilled' in order.keys():
            abort(403, message= 'The order has already been fulfilled')
        order = m.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': status},
            {'returnNewDocument': 'true'})
        
        func.abort_if_not_exist(order)
        resp = dumps(order)
        return make_response(resp, 200)

class OrderDetails(Resource):
    def get(self,id):
        pass
