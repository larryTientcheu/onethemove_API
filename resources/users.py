from re import escape
import sys
from flask import jsonify
from flask.globals import request
from flask_restful import Resource, abort
from bson.json_util import default, dumps
from werkzeug.security import generate_password_hash, check_password_hash


class Users(Resource):
    m = None

    def setMongo(mongo):
        Users.m = mongo

    def get(self):
        users = self.m.db.users.find()
        resp = dumps(users)
        return resp

    

    def abort_if_not_exist(self,email,users):
        if email not in users['email']:
            abort(404, message="Could not find video...")

    def abort_if_exist(self,email,users):

        if email in users:
            abort(409, message="Video already exists with that ID...")

    def put(self, email):
        users = Users.get(self)
        Users.abort_if_exist(self,email,users)
        _json = request.json
        _fname = _json['first_name']
        _lname = _json['last_name']
        _email = _json['email']
        _pwd = _json['password']

        if (_fname or _lname) and _email and _pwd:
            _hashed_pwd = generate_password_hash(_pwd)
            id = Users.m.db.users.insert(
                {'first_name': _fname, 'last_name': _lname, 'email': _email, 'password': _hashed_pwd})

        resp = jsonify("User added successfully")
        resp.status_code = 200

        return resp
