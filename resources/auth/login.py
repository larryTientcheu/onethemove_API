from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_restful import Resource, abort
from flask.globals import request
from codes.functions import Functions
from flask import jsonify, make_response


func = Functions()


def Login_setMongo(mongo):
    global m
    m = mongo
    m = m.db.users


class Login(Resource):

    def post(self):
        _json = request.json
        if 'email' and 'password' not in _json.keys():
            abort(400, message='The request is not formated correctly')
        _email = _json['email']
        users = m.find_one({'email': _email})
        _password = _json['password']
        if users is None:
            abort(404, message="No user exists with this Email address")
        else:
            if func.checkPassword(users['password'], _password):
                users.pop('password')
                resp = make_response(dumps(users), 200)
                resp.mimetype = 'application/json'
                return resp
            else: 
                abort(409, message="Incorrect Email or Password")
            

