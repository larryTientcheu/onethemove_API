
import imp
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource,reqparse,abort
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from resources.users import *
from resources.restaurant import *
from resources.orders import *
from resources.auth.login import *
from resources.auth.register import *



app = Flask(__name__)
app.secret_key ="secretkey"
api = Api(app)

app.config['MONGO_URI'] = "mongodb://localhost:27017/quickmunch"
m = PyMongo(app)

User_setMongo(m)
api.add_resource(Users,"/user", methods=['GET']) # get user. This query should be restricted only to The owner
api.add_resource(User, "/user/<string:id>") # get a specific user and update
api.add_resource(UserCredentials, "/user/<string:id>/<string:credential>", methods=['PUT'])
api.add_resource(U_Address, "/user/address/<string:id>/<int:a>") # get and update adrress, last argument specifies which address



Restaurant_setMongo(m)
api.add_resource(Restaurants, "/restaurant", methods=['GET'])
api.add_resource(Restaurant, "/restaurant/<string:restaurant_id>", methods=['GET', 'PUT'])
api.add_resource(RestaurantCredentials, "/restaurant/<string:restaurant_id>/<string:credential>", methods=['PUT'])
api.add_resource(RestaurantItem, "/restaurant/<string:restaurant_id>/<string:item>", methods=['POST','PUT'])
api.add_resource(RestaurantMealsItem, "/restaurant/<string:restaurant_id>/meals/<int:item_index>", methods=['PUT'])
api.add_resource(RestaurantMealsItemItem, "/restaurant/<string:restaurant_id>/meals/<int:item_index>/<string:item_item>", methods=['PUT'])



Order_setMongo(m)
api.add_resource(Orders, "/order")
api.add_resource(Order, "/order/<string:id>")
api.add_resource(OrderDetails, "/order/<string:id>/detail")

Login_setMongo(m)
api.add_resource(Login, "/login")

Register_setMongo(m)
api.add_resource(RegisterUser, "/register/user")
api.add_resource(RegisterRestaurant, "/register/restaurant")

if __name__ == '__main__':
    app.run(debug=True)


# Put all the requests in a try catch to make sure they are valid requests