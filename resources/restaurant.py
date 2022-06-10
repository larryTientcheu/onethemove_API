from flask import make_response
from flask.globals import request
from flask_restful import Resource, abort
from bson.json_util import dumps
from bson.objectid import ObjectId
from codes.functions import Functions
from codes.dbfunc import RestaurantFunctions
from codes.queries import RestaurantQueries


def Restaurant_setMongo(mongo):
    global m
    m = mongo
    m = m.db.restaurant

func = Functions()
rFuncs = RestaurantFunctions()
rQueries = RestaurantQueries()


class Restaurants(Resource):
    def get(self): # find all restaurants
        parameters = request.args
        param = parameters.get('item')
        
        if param == 'feedbacks':
            restaurant = m.aggregate([{'$project':{'feedbacks':1, 'name':1, 'imgs':1}}])
        else:
            restaurant = m.find({},{'password':0})
        resp = make_response(dumps(restaurant), 200)
        resp.mimetype = 'application/json'
        return resp

class Restaurant(Resource):

    def get(self, restaurant_id):
        restaurant = m.find_one({'_id': ObjectId(restaurant_id)})
        func.abort_if_not_exist(restaurant, "restaurant")
        resp = make_response(dumps(restaurant), 200)
        resp.mimetype = 'application/json'
        return resp
        
    def put(self, restaurant_id):
        # add restaurant password update functions(resource) if password parameter is present
        _json = request.json
        restaurant = m.find_one({'_id': ObjectId(restaurant_id)})
        func.abort_if_not_exist(restaurant, "restaurant")
        restaurant = rFuncs.formatUpdateRestaurant(_json)
        operation = {'$set': restaurant}
        resp = rQueries.updateRestaurant(m,restaurant_id,operation,[])
        return resp


class RestaurantCredentials(Resource):
    def put(self, restaurant_id, credential):
        _json = request.json
        restaurant = m.find_one({'_id': ObjectId(restaurant_id)})
        func.abort_if_not_exist(restaurant, "restaurant")

        if credential == "name":
            if 'name' not in _json.keys():
                abort(400, message= "you must include a new restaurant name to update name")
            _name = _json['name']
            restaurants = m.find_one({'name': _name})
            func.abort_if_exist(restaurants)
            _name = {"name": _name}
            resp = rQueries.updateRestaurantCredentials(m, restaurant_id, _name)
            return resp
            
        elif credential == "email":
            if 'new_email' not in _json.keys():
                abort(400, message= "you must include a new restaurant email to update email")
            _email = _json['new_email']
            restaurants = m.find_one({'email':_email})
            func.abort_if_exist(restaurants)
            _email = {"email": _email}
            resp = rQueries.updateRestaurantCredentials(m, restaurant_id, _email)
            return resp

        elif credential == "password":
            if 'old_password' not in _json.keys() or 'new_password' not in _json.keys():
                abort(400, message="Not all the password parameters were passed")

            hashed_old_password = restaurant['password']
            unhashed_old_password = _json['old_password']
            newPassword = _json['new_password']
            if func.checkPassword(hashed_old_password, unhashed_old_password):
                newPassword = func.hashPassword(newPassword)
                newPassword = {"password": newPassword}
                resp = rQueries.updateRestaurantCredentials(m, restaurant_id, newPassword)
                return resp
            else:
                abort(400, message="Old password doesn't match")



class RestaurantItem(Resource):

    def post(self, restaurant_id, item):
        _json = request.json
        restaurant = m.find_one({'_id': ObjectId(restaurant_id)}) #limit the return keys
        func.abort_if_not_exist(restaurant, "restaurant")
        resp = make_response("bad request", 400)
        arrayFilters = []
        operation = {}

        if item == "drinks":
            operation = rFuncs.updateDrinks(_json)
            resp = rQueries.updateRestaurant(m, restaurant_id, operation, [])
        elif item == "meal":
            # operation, arrayFilters = rFuncs.addMeal(_json)
            operation = rFuncs.addMeal(restaurant, _json)
            resp = rQueries.updateRestaurant(m, restaurant_id, operation, arrayFilters)

        
        return resp

    def put(self, restaurant_id, item):
        _json = request.json
        restaurant = m.find_one({'_id': ObjectId(restaurant_id)})
        func.abort_if_not_exist(restaurant, "restaurant")

        if item == "address":
            _address = rFuncs.formatRestaurantAddress(_json)
            operation = {'$set':{"address": _address}}
            resp = rQueries.updateRestaurant(m, restaurant_id, operation, [])
            return resp

        elif item == "availability":
            _availability = rFuncs.formatRestaurantAvailability(_json)
            operation = {'$set': {"availability": _availability}}
            resp = rQueries.updateRestaurant(m, restaurant_id, operation, [])
            return resp

        elif item =="drink":
            # can only update drinks that exists already
            operation = rFuncs.updateDrinks(_json)
            resp = rQueries.updateRestaurant(m, restaurant_id, operation, [])
            return resp

        elif item =="feedbacks":
            operation = rFuncs.updateRestaurantFeedback(_json)
            resp = rQueries.updateRestaurant(m, restaurant_id, operation, [])
            return resp

        elif item =="images":
            operation = rFuncs.updateImgs(restaurant_id, _json)
            resp = rQueries.updateRestaurant(m, restaurant_id, operation, [])
            return resp

        else:
            abort(404, message="This resource doesn't exist yet")

class RestaurantMealsItem(Resource):
    def put(self, restaurant_id, item_index):
            _json = request.json
            restaurant = m.find_one({'_id': ObjectId(restaurant_id)})
            func.abort_if_not_exist(restaurant, "restaurant")

            for i in _json['meal'].keys():
                updateOperation = "meals.{}.{}".format(item_index, i)
                operation = {'$set': {updateOperation: _json['meal'][i]}}
                resp = rQueries.updateRestaurant(m, restaurant_id, operation, [])
            return resp
        
class RestaurantMealsItemItem(Resource):
    def put(self, restaurant_id, item_index, item_item):
        restaurant = m.find_one({'_id': ObjectId(restaurant_id)})
        func.abort_if_not_exist(restaurant, "restaurant")

        if item_item == "feedbacks":
            _json = request.json
            operation = rFuncs.updateMealFeedback(item_index, _json)
            resp = rQueries.updateRestaurant(m, restaurant_id, operation, [])
        
        elif item_item == "images":
            _json = request.json
            operation = rFuncs.updateMealImg(restaurant_id, item_index, _json)
            resp = rQueries.updateRestaurant(m, restaurant_id, operation, [])
        else:
            abort(404, message="This resource doesn't exist")

        return resp

        #DELETE WILL BE DONE

