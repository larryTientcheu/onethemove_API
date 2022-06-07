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
    global m,mU,mR
    m = mongo
    mU = mongo
    mR = mongo
    m = m.db.orders
    mU = mU.db.users
    mR = mR.db.restaurant

class Orders(Resource):
    def get(self):
        orders = m.find()
        resp = make_response(dumps(orders), 200)
        resp.mimetype = 'application/json'
        return resp

    def post(self):
        _json = request.json
        order = oFunc.formatAddOrder(mU, mR, _json)
        resp = oQueries.addOrder(m, order)
        return resp
class Order(Resource):
    def get (self, id):
        order = m.find_one({'_id': ObjectId(id)})
        func.abort_if_not_exist(order, "order")
        resp = make_response(dumps(order), 200)
        resp.mimetype = 'application/json'
        return resp

    def put(self, id):
        _json = request.json
        order = m.find_one({'_id': ObjectId(id)})
        func.abort_if_not_exist(order, "order")
        if 'date_fulfilled' in order.keys():
            abort(403, message= 'The order has already been fulfilled')
 
        status = oFunc.formatUpdateOrder(_json)
        resp = oQueries.updateOrder(m, id, status)
        return resp

class OrderDetails(Resource):
    def get(self, id):
        order = oFunc.formatDetailedOrder(m, id)
        resp = make_response(dumps(order), 200)
        resp.mimetype = 'application/json'
        return resp

class OrderEntityDetails(Resource):
    def get(self, entity, id):
        if entity == "user":
            order_detailed = oFunc.getOrderEntityDetails(m, entity, id)
            resp = make_response(dumps(order_detailed), 200)
        resp.mimetype = 'application/json'
        return resp

