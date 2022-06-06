from flask import make_response
from flask.globals import request
from flask_restful import Resource, abort
from bson.json_util import dumps
from flask_restful import abort
from codes.dbfunc import AuthFunctions
from codes.queries import AuthQueries

fAuth = AuthFunctions()
qAuth = AuthQueries()

def Register_setMongo(mongo):
    global mU,mR
    mU = mongo
    mR = mongo
    mU = mU.db.users
    mR = mR.db.restaurant


class RegisterUser(Resource):
    def post(self):
        _json = request.json
        if 'first_name' not in _json.keys() or 'email' not in _json.keys() or 'password' not in _json.keys():
            abort(400, message="Not all the parameters are present")
        
        user = fAuth.formatRegisterUser(mU, _json)
        resp = qAuth.registerUser(mU, user)
        resp = make_response("registered", 201)
        return resp

class RegisterRestaurant(Resource):
    def post(self):
        pass