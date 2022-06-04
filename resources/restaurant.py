from datetime import datetime
from re import escape
from flask import jsonify, make_response
from flask.globals import request
from flask_restful import Resource, abort
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from codes.functions import Functions
import codes.dbfunc as dbfunc
import codes.queries as query


def Restaurant_setMongo(mongo):
    global m
    m = mongo
    m = m.db.restaurant

func = Functions()


class Restaurants(Resource):
    def get(self): # find all restaurants
        restaurant = m.find()
        resp = dumps(restaurant)
        return make_response(resp, 200)

    
    def post(self):

        _json = request.json
        if 'email' not in _json.keys() and 'name' not in _json.keys() and 'password' not in _json.keys():
            abort(400, message='The request is not formated correctly')
        _email = _json['email']
        restaurants = m.find_one({'email': _email})
        func.abort_if_exist(restaurants)
        _name = _json['name']
        _description = _json['description']
        _pwd = _json['password']
        _tags = _json['tags']
        

        # All the feilds below this will be empty on creation. Will be updated on later
        # Add seperate resource for add drinks meals etc
        _availability = {}
        _address = {}
        _drinks = []
        _delivery_time = 0
        _meals = []
        _imgs = []
        _feedback = {}

        if _name and _email and _pwd:
            _hashed_pwd = generate_password_hash(_pwd)
            id = m.insert(
                {'address':_address, 'name': _name, 'description': _description, 'email': _email, 'password': _hashed_pwd,
                'tags': _tags, 'availability': _availability, ' drinks': _drinks,
                'delivery_time':_delivery_time, 'meals': _meals, 'img': _imgs, 'feedback':_feedback
                }
            )
            
        resp = dumps(id)

        return make_response(resp, 200)


def formatRestaurantAddress(_json):
    _loc = [_json['address']['lat'], _json['address']['lon']]
    _address = {'manager_name': _json['address']['manager_name'], 'restaurant_phone': _json['address']['restaurant_phone'],
    'manager_phone': _json['address']['manager_phone'], 'neighbourhood': _json['address']['neighbourhood'],
    'town': _json['address']['town'], 'loc':_loc}

    return _address




def formatAvailability(_json):
    _availability = {'mon': _json['availability']['mon'], 'tue': _json['availability']['tue'],
    'wed': _json['availability']['wed'], 'thur': _json['availability']['thur'],
    'fri': _json['availability']['fri'], 'sat': _json['availability']['sat'],
    'sun': _json['availability']['sun']}

    return _availability



def formatImgs(_json):
    _restaurantEmail = _json['email']
    _imgs = []
    for i in _json['imgs']:
        _imgs.append("{}/{}".format(_restaurantEmail,_json['imgs'][i]))
    
    return _imgs


class Restaurant(Resource):

    def get(self, id):
        restaurant = m.find_one({'_id': ObjectId(id)})
        func.abort_if_not_exist(restaurant)
        resp = dumps(restaurant)
        return resp

    def post(self, id):
        _json = request.json
        if 'drinks' in _json.keys():
            operation = dbfunc.addDrink(_json)
        elif 'meal' in _json.keys():
            operation = dbfunc.addMeal(_json)

        m.update_one(
            {'_id': ObjectId(id)},
            update = operation, 
            upsert=False
        )
        return make_response("Added", 200)
        
    def put(self, id):
        _json = request.json
        operation = {}
        arrayFilters ={}
        # This can update the other fields depending on the json parameter passed except tags, address, availability, menu, drinks, imgs, and feedback.
        if 'address' in _json.keys():
            _address = formatRestaurantAddress(_json)
            _json['address'] = _address

        if 'availability' in _json.keys():
            _availability = formatAvailability(_json)
            _json['availability'] = _availability
        
        
        if 'meal' not in _json.keys() and 'drinks'  not in _json.keys() and 'imgs' not in _json.keys():
            operation = {'$set': _json}
            arrayFilters = []
        else:
            if 'drinks' in _json.keys():
                operation, arrayFilters = dbfunc.updateDrinks(_json)
            # elif 'imgs' in _json.keys():
            #     _imgs = formatImgs(_json)
            #     operation = {'$addToSet': {"imgs":{'$each':_imgs}}} #for image
            elif 'meal' in _json.keys():
                resp = dbfunc.updateMeal(m, id, _json)
                # resp = dbfunc.updateMeal(m, id, _json)
        

        # Should be in try/catch doesn't return anything
        #query.updateRestaurant(m, operation, arrayFilters)

        return resp

        #DELETE WILL BE DONE

