import codes.queries as query
from bson.objectid import ObjectId
from datetime import datetime

def addDrink(_json):
    # A drink comes in as an object. added one at a time
    operation = {'$addToSet': {"drinks":{'$each': [_json['drinks']]}}}
    return operation

def updateDrinks(_json):
    # A drink comes in as an object.
    operation = {'$set': {"drinks.$[elem]":_json['drink']}}
    arrayFilters = [{"elem.name": {'$eq':_json['drink']['name']}}]
    return operation, arrayFilters

def addMeal(_json):
    _json['meal']['feedback'] = []
    _json['meal']['img'] = []
    operation = {'$addToSet': {'meals': {'$each': [_json['meal']]}}}
    return operation

def formatFeedback(_json):
    _user = ObjectId(_json['feedback']['user'])
    _rating = _json['feedback']['rating']
    _comment = _json['feedback']['comment']
    _date = datetime.now()
    
    _feedback = {'user':_user, 'rating':_rating, 'comment':_comment, 'date':_date}
    return _feedback

def updateMeal(m, id, _json):

    _json['meal']['feedbacks'] = []
    operation ={'$set': {"meals.$[elem]": _json['meal']}}
    arrayFilters = [{"elem.name": {'$eq': _json['meal']['name']}}]
    resp = query.updateRestaurant(m, id, operation, arrayFilters)

    operation = addMealImg(_json['imgs'])
    resp = query.updateRestaurant(m, id, operation, [])

    operation = addFeedback(_json['feedbacks'])
    resp = query.updateRestaurant(m, id, operation, [])
    
    return resp

def addFeedback(_json):
    # json feedback is an array
    operation = {'$set': {"meals.$[].feedbacks":_json}}
    return operation

def addMealImg(_json):
    operation = {'$set':{"meals.$[].imgs":_json}}
    return operation
