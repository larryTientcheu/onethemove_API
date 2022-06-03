from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_restful import Resource, abort
from flask import make_response
from flask.globals import request
from datetime import datetime
from codes.functions import Functions

func = Functions()
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
        # Add check if user exists and restaurant exists
        _user = ObjectId(_json['user'])
        _restaurant = ObjectId(_json['restaurant'])
        _address = _json['address']
        _item = {'restaurant': _restaurant,'menu':{'drink': _json['drink'], 'meal': _json['meal']}} 
        # drinks and meal represent the index of the array containing them
        _date_created = datetime.today()
        #if date fulfilled key is not present then order has not yet been fulfilled. This is updated only when the status of delivered is set to true.
        _status = 'preparing'

        if _user and _address and _json['restaurant'] and _date_created:
            id = m.insert(
                {'user':_user, 'address':_address, 'item':_item, 'date_created':_date_created,
                'status':_status})
                
            resp = dumps(id)
            return make_response(resp, 200)
        else:
            message = 'Error while adding an order'
            abort(400, message=message)

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
