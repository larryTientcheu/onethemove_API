from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource,reqparse,abort
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

from resources.users import Users


app = Flask(__name__)
app.secret_key ="secretkey"
api = Api(app)

app.config['MONGO_URI'] = "mongodb://localhost:27017/quickmunch"
m = PyMongo(app)

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not found ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

Users.setMongo(m)
api.add_resource(Users,"/users/new")


if __name__ == '__main__':
    app.run(debug=True)