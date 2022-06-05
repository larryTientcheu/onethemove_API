from bson.objectid import ObjectId
from datetime import datetime
from flask_restful import abort
from werkzeug.security import generate_password_hash, check_password_hash
from codes.functions import Functions
func = Functions()


class  RestaurantFunctions():
    def formatAddRestaurant(self, m, _json):
        if 'email' not in _json.keys() or 'name' not in _json.keys() or 'password' not in _json.keys():
            abort(400, message='The request is not formated correctly')
        _email = _json['email']
        restaurants = m.find_one({'email': _email})
        func.abort_if_exist(restaurants)
        _name = _json['name']
        _description = _json['description']
        _pwd = _json['password']
        _tags = _json['tags']
        
        # All the feilds below this will be empty on creation. Will be updated on later

        if not _name or not _email or not _pwd:
            abort(400, message="The request is not formated correctly name email and restaurant")
        else:
            _hashed_pwd = generate_password_hash(_pwd)
            restaurant = {'name': _name, 'description': _description, 'email': _email, 'password': _hashed_pwd,
                'tags': _tags
                }
            return restaurant

    def formatUpdateRestaurant(self, _json):
            if 'email' not in _json.keys() or 'name' not in _json.keys() or 'password' not in _json.keys():
                abort(400, message='The request is not formated correctly')
            _email = _json['email']
            _name = _json['name']
            _description = _json['description']
            _pwd = _json['password']
            _tags = _json['tags']
            
            # All the feilds below this will be empty on creation. Will be updated on later

            if not _name or not _email or not _pwd:
                abort(400, message="The request is not formated correctly name email and restaurant")
            else:
                _hashed_pwd = generate_password_hash(_pwd)
                restaurant = {'name': _name, 'description': _description, 'email': _email, 'password': _hashed_pwd,
                    'tags': _tags
                    }
                return restaurant

    def formatRestaurantAddress(self, _json):
        if 'address' in _json.keys():
            _loc = [_json['address']['lat'], _json['address']['lon']]
            _address = {'manager_name': _json['address']['manager_name'], 'restaurant_phone': _json['address']['restaurant_phone'],
            'manager_phone': _json['address']['manager_phone'], 'neighbourhood': _json['address']['neighbourhood'],
            'town': _json['address']['town'], 'loc':_loc}
        
        else:
            abort(400, message="The request address is not formated correctly")

        return _address

    def formatRestaurantAvailability(self, _json):
        if 'availability' in _json.keys():
            _availability = {'mon': _json['availability']['mon'], 'tue': _json['availability']['tue'],
            'wed': _json['availability']['wed'], 'thur': _json['availability']['thur'],
            'fri': _json['availability']['fri'], 'sat': _json['availability']['sat'],
            'sun': _json['availability']['sun']}
        else:
            abort(400, message="The request availability is not formated correctly")

        return _availability

    def updateDrinks(self, _json):
        # A drink comes in as an array of drinks. Replaces everything same as add Drink.
        if 'drinks' in _json.keys():
            operation = {'$set': {"drinks": _json['drinks']}}
            return operation
        else:
            abort(400, message="The request drinks is not formated correctly")

    def formatImgs(self, id, images):
        _imgs = []
        print()
        for i in images:
            _imgs.append("{}/{}".format(id,i))
        
        return _imgs

    def updateImgs(self, id,_json):
        # Same Function for add 
        if 'imgs' in _json.keys():
            imgs = self.formatImgs(id, _json['imgs'])
            operation = {'$set': {"imgs": imgs}}
            return operation
        

    def addMeal(self, _json):
        _json['meal']['feedback'] = []
        _json['meal']['img'] = []
        operation = {'$addToSet': {'meals': {'$each': [_json['meal']]}}}
        return operation

    def formatFeedback(self, _json):

        feedback = []
        # add Checks for rating
        for i in _json:
            _user = ObjectId(i['user'])
            _rating = i['rating']
            _comment = i['comment']
            _date = datetime.now()
            feedback.append({'user':_user, 'rating':_rating, 'comment':_comment, 'date':_date})

        return feedback

    def updateFeedback(self, meal_index, _json):
        # json feedback is an array
        if "feedbacks" not in _json.keys():
            abort(400, message="The request feedback is not formated correctly")

        _feedback = self.formatFeedback(_json['feedbacks'])
        operation = {'$addToSet': {"meals.{}.feedbacks".format(meal_index):{'$each': _feedback}}}
        return operation

    def updateMealImg(self, meal_index, _json):
        if "imgs" not in _json.keys():
            abort(400, message="The request feedback is not formated correctly")
        
        operation = {'$set':{"meals.{}.imgs".format(meal_index): _json['imgs']}}
        return operation

class OrderFunctions():

    def formatAddOrder(self, _json):
        # Add check if user exists and restaurant exists

        if 'user' not in _json.keys() or 'restaurant' not in _json.keys() or 'address' not in _json.keys() or 'meal' not in _json.keys():
            abort(40, 'request not formatted correctly')

        _user = ObjectId(_json['user'])
        _restaurant = ObjectId(_json['restaurant'])
        _address = _json['address']
        
        if 'drink' not in _json.keys():
            _drink = None
        else:
            _drink = _json['drink'] 

        _item = {'restaurant': _restaurant,'menu':{'drink': _drink, 'meal': _json['meal']}} 
        # drinks and meal represent the index of the array containing them
        _date_created = datetime.today()
        #if date fulfilled key is not present then order has not yet been fulfilled. This is updated only when the status of delivered is set to true.
        _status = 'preparing'

        order = {'user':_user, 'address':_address, 'item':_item, 'date_created':_date_created,
                'status':_status}
                
        return order


    def formatUpdateOrder(self, _json):
        _status = _json['status']
        order = {'status': _status}
        if _status == 'delivered':
            _date_fulfilled = datetime.today()
            order = {'status': _status, 'date_fulfilled': _date_fulfilled}
        return order
