
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource,reqparse,abort
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

from resources.users import User_setMongo,Users,User,U_Address
from resources.restaurant import Restaurant, Restaurant_setMongo, Restaurants



app = Flask(__name__)
app.secret_key ="secretkey"
api = Api(app)

app.config['MONGO_URI'] = "mongodb://localhost:27017/quickmunch"
m = PyMongo(app)

User_setMongo(m)
api.add_resource(Users,"/users") # get and add users
api.add_resource(User, "/user/<string:id>") # get a specific user and update
api.add_resource(U_Address, "/user/address/<string:id>/<int:a>") # get and update adrress, last argument specifies which address



Restaurant_setMongo(m)
api.add_resource(Restaurants, "/restaurant")
api.add_resource(Restaurant, "/restaurant/<string:id>")

if __name__ == '__main__':
    app.run(debug=True)