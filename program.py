from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource,reqparse,abort
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

#from resources.users import Users
from resources.users import setMongo,Users,User,Address1,Address2


app = Flask(__name__)
app.secret_key ="secretkey"
api = Api(app)

app.config['MONGO_URI'] = "mongodb://localhost:27017/quickmunch"
m = PyMongo(app)

setMongo(m)
api.add_resource(Users,"/users")
api.add_resource(User, "/user/<string:id>")
api.add_resource(Address1, "/address/<string:id>")
api.add_resource(Address2, "/address2/<string:id>")


if __name__ == '__main__':
    app.run(debug=True)