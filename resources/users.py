from re import escape
import sys
import json
from bson import json_util
from flask import make_response
from flask.globals import request
from flask_restful import Resource, abort
from bson.json_util import default, dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from codes.functions import Functions



func = Functions()

def User_setMongo(mongo):
    global m
    m = mongo
    m = m.db.users

class Users(Resource):

    def get(self):  # find all users
        users = m.find()
        resp = dumps(users)
        resp = make_response(resp, 200)
        resp.mimetype = 'application/json'
        return resp


    # Seperate create user and adress(Personal resource and also for cart)
    # This should be added as a resource Register
    def post(self):  # add

        _json = request.json
        _fname = _json['first_name']
        _lname = _json['last_name']
        _email = _json['email']
        #_birthday = _json['birthday']
        _pwd = _json['password']
        _address1 = {} #Empty address on creation of user now. should fix to create with user with if empty leave but enforce later
        _address2 = {}
        _cart = []
        "sdsdsd"

        user = m.find_one({'email': _email})
        func.abort_if_exist(user)

        if (_fname or _lname) and _email and _pwd:
            _hashed_pwd = func.hashPassword(_pwd)
            id = m.insert(
                {'address1': _address1,'address2': _address2, 'first_name': _fname, 'last_name': _lname, 'email': _email, 'password': _hashed_pwd, 'cart': _cart})
            # the above line inserts the elements in the database if the user doesn't exist
            resp = make_response(dumps(id), 201)
            resp.mimetype = 'application/json'
            return resp
        else:
            message = 'Error while adding a user'
            abort(400, message=message)


class User(Resource):

    def get(self, id):

        user = m.find_one({'_id': ObjectId(id)})
        func.abort_if_not_exist(user, "user")
        resp = make_response(dumps(user), 200)
        resp.mimetype = 'application/json'
        return resp
  


    def put(self, id):

        _json = request.json
        # This can update the other fields depending on the json parameter passed except address and cart
        # Update user password as a seperate resource
        user = m.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': _json},
            {'returnNewDocument': 'true'}
        )
        func.abort_if_not_exist(user)
        resp = dumps(user)
        return make_response(resp, 200)

        # DELETE Will be done

def formatAddress(_json): # This json is a basic json object look at notes
    _loc = [_json['lat'], _json['lon']]
    _address = {'neighbourhood': _json['neighbourhood'],
    'town': _json['town'], 'loc':_loc}
         
    return _address
class U_Address(Resource):
    def get(self, id, a):
        user = m.find_one({'_id': ObjectId(id)})
        func.abort_if_not_exist(user)
        if a == 1:
            address = user['address1']
        else:
            address = user['address2']

        resp = dumps(address)
        return resp

    def put(self, id, a):  # Updates or create a new address1 Should be reviewed
        _json = request.json
        _address = formatAddress(_json)
                    
        if a == 1:
            address = m.find_one_and_update(
                {'_id': ObjectId(id)},
                {'$set': {'address1': _address}},
                {'returnNewDocument': 'true'}
            )
            func.abort_if_not_exist(address)
        else:
            address = m.find_one_and_update(
                {'_id': ObjectId(id)},
                {'$set': {'address2': _address}},
                {'returnNewDocument': 'true'}
            )
            func.abort_if_not_exist(address)

        resp = dumps(address)
        return make_response(resp, 200)


# FORMAT CART