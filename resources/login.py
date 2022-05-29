from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_restful import Resource, abort
from flask.globals import request
from codes.functions import Functions
from flask import jsonify


func = Functions()


def Login_setMongo(mongo):
    global m
    m = mongo
    m = m.db.users


class Login(Resource):

    def get(self):
        _json = request.json
        _email = _json['email']
        users = m.find_one({'email': _email})
        _password = _json['password']
        if users is None:
            abort(404, message="No user exists with this email address")
        else:
            if func.checkPassword(users['password'], _password):
                users.pop('password')
                return dumps(users)
            else: return False
            

