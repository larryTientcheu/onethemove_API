import codes.queries as query
from bson.objectid import ObjectId
from datetime import datetime

def addDrink(_json):
    # A drink comes in as an object. added one at a time
    operation = {'$addToSet': {"drinks":{'$each': [_json['drinks']]}}}
    return operation

def updateDrinks(_json):
    # A drink comes in as an object.
    operation = {'$set': {"drinks.$[elem]":_json['drinks']}}
    arrayFilters = [{"elem.name": {'$eq':_json['drinks']['name']}}]
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
    print('sdasds')
    if 'feedbacks'  in _json.keys():
        _json['meal']['feedbacks'] = []
        operation ={'$set': {"meals.$[elem]": _json['meal']}}
        arrayFilters = [{"elem.name": {'$eq': _json['meal']['name']}}]
        resp = query.updateRestaurant(m, id, operation, arrayFilters)

        #_feedbacks = formatFeedback(_json)
        #_json['feedback'] = _feedbacks
        operation = addFeedback(_json['feedbacks'])
        # arrayFilters = [{"elem.name.feedbacks.elem1.comment": {'$eq': _json['feedback']['comment']}}]
        resp = query.updateRestaurant(m, id, operation, [])
    
    return resp

def addFeedback(_json):
    # json feedback is an array
    operation = {'$set': {"meals.$[].feedbacks":_json}}
    return operation
