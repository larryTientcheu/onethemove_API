from re import escape
import sys
from flask import jsonify
from flask.globals import request
from flask_restful import Resource, abort
from bson.json_util import default, dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


def setMongo(mongo):
    global m
    m = mongo
    m = m.db.users


class Users(Resource):

    def get(self):  # find all users
        users = m.find()
        resp = dumps(users)
        return resp

    def abort_if_not_exist(self, email, users):
        if email not in users['email']:
            abort(404, message="Could not find user...")

    def abort_if_exist(self, email, users):

        if email in users:
            abort(409, message="User already exists with that email ID...")

    # Seperate create user and adress(Personal resource and also for cart)
    def post(self):  # add
        users = Users.get(self)

        _json = request.json
        _fname = _json['first_name']
        _lname = _json['last_name']
        _email = _json['email']
        #_birthday = _json['birthday']
        _pwd = _json['password']
        
        '''_loc = [_json['lat'],_json['lon']]
        _address = {'neighbourhood': _json['neighbourhood'], 'town': _json['town'], 'loc':_loc}'''
        _address1 = {} #Empty address on creation of user
        _address2 = {}
        _cart = []

        Users.abort_if_exist(self, _email, users)

        if (_fname or _lname) and _email and _pwd:
            _hashed_pwd = generate_password_hash(_pwd)
            id = m.insert(
                {'address1': _address1,'address2': _address2, 'first_name': _fname, 'last_name': _lname, 'email': _email, 'password': _hashed_pwd, 'cart': _cart})
            # print(id)

        resp = jsonify(dumps(id))
        resp.status_code = 200

        return resp


class User(Resource):

    def get(self, id):
        users = m.find_one({'_id': ObjectId(id)})
        resp = dumps(users)
        return resp

    def put(self, id):

        _json = request.json
        # This can update the other fields depending on the json parameter passed except address and cart

        user = m.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': _json},
            {'returnNewDocument': 'true'}
        )
        resp = dumps(user)
        return resp

        # DELETE Will be done


class Address1(Resource):
    def get(self, id):
        user = m.find_one({'_id': ObjectId(id)})
        # print(user['address1'])
        address = user['address1']

        resp = dumps(address)
        return resp

    def put(self, id):  # Updates or creat a new address1
        _json = request.json
        _loc = [_json['lat'], _json['lon']]
        _address = {'neighbourhood': _json['neighbourhood'],
                     'town': _json['town'], 'loc':_loc}
                    
        print(_address)

        address = m.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': {'address1': _address}},
            {'returnNewDocument': 'true'}
        )

        resp = dumps(address)
        return resp


class Address2(Resource):
    def get(self, id):
        user = m.find_one({'_id': ObjectId(id)})
        # print(user['address1'])
        address = user['address2']

        resp = dumps(address)
        return resp

    def put(self, id):  # Updates or creat a new address1
        _json = request.json
        _loc = [_json['lat'], _json['lon']]
        _address = {'neighbourhood': _json['neighbourhood'],
                     'town': _json['town'], 'loc':_loc}
                    
        print(_address)

        address = m.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': {'address2': _address}},
            {'returnNewDocument': 'true'}
        )

        resp = dumps(address)
        return resp