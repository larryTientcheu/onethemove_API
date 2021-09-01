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
  
    def get(self): #find all users
        users = m.find()
        resp = dumps(users)
        return resp
    
    def abort_if_not_exist(self,email,users):
        if email not in users['email']:
            abort(404, message="Could not find video...")

    def abort_if_exist(self,email,users):

        if email in users:
            abort(409, message="Video already exists with that ID...")

    def post(self): #add
        users = Users.get(self)
        
        _json = request.json
        _fname = _json['first_name']
        _lname = _json['last_name']
        _email = _json['email']
        #_birthday = _json['birthday']
        _pwd = _json['password']
        _loc = [_json['lat'],_json['lon']]
        _address = [{'neighbourhood': _json['neighbourhood'], 'town': _json['town'], 'loc':_loc}]
        _cart = []

        Users.abort_if_exist(self,_email,users)

        if (_fname or _lname) and _email and _pwd:
            _hashed_pwd = generate_password_hash(_pwd)
            id = m.insert(
                {'adresses': _address,'first_name': _fname, 'last_name': _lname, 'email': _email, 'password': _hashed_pwd, 'cart':_cart})
            #print(id)

        resp = jsonify(dumps(id))
        resp.status_code = 200

        return resp

    

class User(Resource):
   
    def get(self, id):
        users = m.find_one({'_id': ObjectId(id)})
        resp = dumps(users)
        return resp


    def put(self,id):
        
        _json = request.json

        user = m.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set':_json},
            {'returnNewDocument':'true'}
            )
        resp = dumps(user)
        return resp

