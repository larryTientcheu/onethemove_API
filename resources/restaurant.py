from re import escape
from flask import jsonify
from flask.globals import request
from flask_restful import Resource, abort
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


def Restaurant_setMongo(mongo):
    global m
    m = mongo
    m = m.db.restaurant

class Restaurants(Resource):
    def get(self): # find all restaurants
        restaurant = m.find()
        resp = dumps(restaurant)
        return resp


    def abort_if_not_exist(self, email, restaurant):
        if email not in restaurant['email']:
            abort(404, message="Could not find Restaurant...")

    def abort_if_exist(self, email, restaurant):
        if email in restaurant:
            abort(409, message="Restaurant already exists with that email ...")
    
    def post(self):

        restaurants = Restaurants.get(self)

        _json = request.json
        _name = _json['name']
        _description = _json['description']
        _email = _json['email']
        _pwd = _json['password']
        

        # All the feilds below this will be empty on creation. Will be updated on second page

        _likes = 0
        _tags = []
        _availability = {}
        _address = {}
        _drinks = []
        _delivery_time = 0
        _min_price = 0
        _meals = []
        _imgs = []
        _city = ""
        _feedback = {}


        Restaurants.abort_if_exist(self, _email, restaurants)

        if _name and _email and _pwd:
            _hashed_pwd = generate_password_hash(_pwd)
            id = m.insert(
                {'address':_address, 'name': _name, 'description': _description, 'email': _email, 'password': _hashed_pwd,
                'likes': _likes, 'tags': _tags, 'availability': _availability, ' drinks': _drinks,
                'delivery_time':_delivery_time, 'min_price':_min_price, 'meals': _meals, 'img': _imgs, 'city': _city,
                'feedback':_feedback
                }
            )

        resp = jsonify(dumps(id))
        resp.status_code = 200

        return resp


class Restaurant(Resource):

    def get(self, id):
        restaurant = m.find_one({'_id': ObjectId(id)})
        resp = dumps(restaurant)
        return resp

    def put(self, id):
        _json = request.json
        # This can update the other fields depending on the json parameter passed except tags, address, availability, menu, drinks, imgs, and feedback.

        restaurant = m.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': _json},
            {'returnNewDocument': 'true'}
        )
        resp = dumps(restaurant)
        return resp

        #DELETE WILL BE DONE

def formatRestaurantAddress(_json):
    _loc = [_json['lat'], _json['lon']]
    _address = {'manager_name': _json['manager_name'], 'restaurant_phone': _json['restaurant_phone'],
    'manager_phone': _json['manager_phone'], 'neighbourhood': _json['neighbourhood'],
    'town': _json['town'], 'loc':_loc}

    return _address

def formatAvailability(_json):
    _availability = {'mon': _json['mon'], 'tue': _json['tue'], 'wed': _json['wed'], 'thur': _json['thur'],
    'fri': _json['fri'], 'sat': _json['sat'], 'sun': _json['sun']}

    return _availability

def formatDrinks(_json):
    _drink = {'name': _json['dname'], 'price':_json['dprice']}
    return _drink


