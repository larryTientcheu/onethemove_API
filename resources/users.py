from ast import arg
from flask import make_response
from flask.globals import request
from flask_restful import Resource, abort, reqparse
from bson.json_util import dumps
from bson.objectid import ObjectId
from numpy import ufunc
from codes.functions import Functions
from codes.dbfunc import AuthFunctions, UserFunctions
from codes.queries import UserQueries



func = Functions()
uFunc = UserFunctions()
uQueries = UserQueries()
authFunc = AuthFunctions()

def User_setMongo(mongo):
    global m
    m = mongo
    m = m.db.users

class Users(Resource):

    def get(self):  # find all users
        users = m.find({},{'password':0})
        resp = dumps(users)
        resp = make_response(resp, 200)
        resp.mimetype = 'application/json'
        return resp

    # Seperate create user and adress(Personal resource and also for cart)
  

class User(Resource):

    def get(self, id):

        user = m.find_one({'_id': ObjectId(id)},{'password':0})
        func.abort_if_not_exist(user, "user")
        resp = make_response(dumps(user), 200)
        resp.mimetype = 'application/json'
        return resp

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        args = parser.parse_args()
        print(args)

        _json = request.json

        user = m.find_one({'_id': ObjectId(id)})
        func.abort_if_not_exist(user, "user")
        # This will update the other fields depending on the json parameter passed except address and cart
        # Update user password as a seperate resource
        user = uFunc.formatUpdateUser(_json)
        resp = uQueries.updateUser(m, id, user)

        return resp
        # DELETE Will be done

class UserCredentials(Resource):
    def put(self, id, credential):
        _json = request.json
        if credential == 'password':
            newPassword = authFunc.formatUpdateUserPassword(m, id, _json)
            newPassword = {"password": newPassword}
            resp = uQueries.updateUser(m, id, newPassword)

        elif credential == 'email':
            new_email = authFunc.formatUpdateUserEmail(m, id, _json)
            new_email = {"email": new_email}
            resp = uQueries.updateUser(m, id, new_email)

        return resp
            


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