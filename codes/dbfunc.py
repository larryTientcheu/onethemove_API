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
        #_meal = [{}]
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
            
            # All the fields not here Will be updated on later

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
        

    def addMeal(self, restaurant, _json):
        # _json['meal']['feedback'] = []
        # _json['meal']['img'] = []
        # # operation = {'$addToSet': {'meals': {'$each': [_json['meal']]}}}
        # operation ={'$set': {"meals.$[elem]":_json['meal']}}
        # arrayFilters = [{"elem.name": {'$ne': _json['meal']['name']}}]
        # return operation, arrayFilters
        if 'meals' not in restaurant.keys():
            restaurant['meals'] = []
        for i in restaurant['meals']:
            if i['name'] == _json['meal']['name']:
                abort(404, message="A restaurant with this name already exists")
        
        operation = {'$push': {"meals": _json['meal']}}

        return operation



    # def put(self, restaurant_id, item_index):
    #     _json = request.json
    #     restaurant = m.find_one({'_id': ObjectId(restaurant_id)})
    #     func.abort_if_not_exist(restaurant, "restaurant")

    #     for i in _json['meal'].keys():
    #         updateOperation = "meals.{}.{}".format(item_index, i)
    #         operation = {'$set': {updateOperation: _json['meal'][i]}}
    #         resp = rQueries.updateRestaurant(m, restaurant_id, operation, [])
    #     return resp

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
    def formatMealDrinkInOrder(self, _json):
        _meal = None
        _drink = None
        if 'meal' not in _json.keys() and 'drink' not in _json.keys():
            abort(400,  message='The order request is badly formatted. A meal or Drink must be included')
        else:
            if 'meal' in _json.keys():
                if _json['meal'] is not None:
                    if 'portion' not in _json['meal'].keys():
                        abort(400,  message='A portion must be included when selecting a meal')
                    _meal = _json['meal']
            if 'drink' in _json.keys():
                if _json['drink'] is not None:
                    _drink = _json['drink']  
            
            if _meal is None and _drink is None:
                abort(400, message="Either a meal or drink must be selected")
        return _meal, _drink

    def formatAddOrder(self, mU, mR, _json):
        # Add check if user exists and restaurant exists

        if 'user' not in _json.keys() or 'restaurant' not in _json.keys() or 'address' not in _json.keys():
            abort(400,  message='request not formatted correctly')
        _user = ObjectId(_json['user'])
        func.abort_if_not_exist(mU.find_one({'_id': _user}), "user")

        _restaurant = ObjectId(_json['restaurant'])
        func.abort_if_not_exist(mR.find_one({'_id': _restaurant}), "restaurant")

        _address = _json['address']
        _meal, _drink = self.formatMealDrinkInOrder(_json)
       
        _date_created = datetime.today().astimezone()
        #if date fulfilled key is not present then order has not yet been fulfilled. This is updated only when the status is set to delivered.
        _status = 'in_cart'

        order = {'user':_user, 'address':_address,'restaurant':_restaurant, 'meal': _meal, 'drink': _drink,
         'date_created':_date_created, 'status':_status}
                
        return order


    def formatUpdateOrder(self, _json):
        # Update order only modifies the status
        if 'status' not in _json.keys():
            abort(400,  message='Status must be specified')
        _status = _json['status']

        if _status == 'in_cart':
            _meal, _drink = self.formatMealDrinkInOrder(_json)
            order = {'meal': _meal, 'drink': _drink, 'status': _status}
        else:
            order = {'status': _status}
        if _status.lower() == 'delivered':
            _date_fulfilled = datetime.today().astimezone()
            order = {'status': _status, 'date_fulfilled': _date_fulfilled}
        return order

    def getOrderDetails(self, m, id):
        operation = m.aggregate([{'$match': {'_id': ObjectId(id)}},
            {'$lookup':{
                'from': "restaurant",
                'localField': "restaurant",
                'foreignField': "_id",
                'as': "Restaurant"
            }
            },{'$project':{"Restaurant.meals.feedbacks":0, "Restaurant.imgs":0,
            "Restaurant.availability":0, "Restaurant.feedback":0, "Restaurant.tags":0,
            "Restaurant.password":0, "Restaurant.description":0, "Restaurant.address":0,   }}
        ])
        return list(operation)
    
    def getOrderedMeal(self, order_detailed, mIndex):
        meal = order_detailed[0]["Restaurant"][0]['meals'][mIndex]
        return meal
    
    def getOrderedDrink(self, order_detailed, dIndex):
        drink = order_detailed[0]["Restaurant"][0]['drinks'][dIndex]
        return drink

    def computeOrderedMealPrice(self, mQuantity, ordered_meal, detail):
        price = mQuantity*ordered_meal['portions'][detail]
        return price

    def computeOrderedDrinkPrice(self, dQuantity, ordered_drink):
        price = dQuantity*ordered_drink['price']
        return price

    def formatProcessOrder(self, m, id, detail):
        order_detailed = self.getOrderDetails(m, id)

        if order_detailed[0]['meal'] is not None:
            mIndex = order_detailed[0]['meal']['index']
            mQuantity = order_detailed[0]['meal']['quantity']
            ordered_meal = self.getOrderedMeal(order_detailed, mIndex)
            #ordered_meal.pop('portions')
            order_detailed[0]['meal'] = ordered_meal
            order_detailed[0]['meal_quantity'] = mQuantity

            print(detail.lower())
            if detail.lower() != "small" and detail.lower() != "medium" and detail.lower() != "large":
                abort(400, message="portion must be either small, medium or large")
            
            order_detailed[0]['meal_portion'] = detail
            oMPrice = ordered_meal['portions'][detail]
            order_detailed[0]['meal_price'] = oMPrice
        
        if order_detailed[0]['drink'] is not None:

            dIndex = order_detailed[0]['drink']['index']
            dQuantity = order_detailed[0]['drink']['quantity']
            ordered_drink =  self.getOrderedDrink(order_detailed, dIndex)
            oDPrice = ordered_drink['price']
            order_detailed[0]['drink'] = ordered_drink
            order_detailed[0]['drink_quantity'] = dQuantity
            order_detailed[0]['drink_price'] = oDPrice
        
        order_detailed[0].pop('Restaurant')
        
        return order_detailed