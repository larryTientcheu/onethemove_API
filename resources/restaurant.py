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
        restaurant = m.find()
        resp = dumps(restaurant)
        return make_response(resp, 200)

    def post(self):
        _json = request.json
        restaurant = rFuncs.formatAddRestaurant(m,_json)
        resp = rQueries.addRestaurant(m, restaurant)
        return resp

class Restaurant(Resource):

    def get(self, restaurant_id):
        restaurant = m.find_one({'_id': ObjectId(restaurant_id)})
        func.abort_if_not_exist(restaurant)
        resp = dumps(restaurant)
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
            operation = rFuncs.updateDrinks( _json)
            resp = rQueries.updateRestaurant(m, restaurant_id, operation, [])
            return resp

        # elif item =="feedbacks":

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
            operation = rFuncs.updateFeedback(item_index, _json)
            resp = rQueries.updateRestaurant(m, restaurant_id, operation, [])
        
        elif item_item == "images":
            _json = request.json
            operation = rFuncs.updateMealImg(item_index, _json)
            resp = rQueries.updateRestaurant(m, restaurant_id, operation, [])
        else:
            abort(404, message="This resource doesn't exist")

        return resp

        #DELETE WILL BE DONE

