from email import message
from bson.objectid import ObjectId
from datetime import datetime
from flask_restful import abort
from sqlalchemy import JSON
from werkzeug.security import generate_password_hash, check_password_hash
from codes.functions import Functions
func = Functions()


class AuthFunctions():
    def formatRegisterUser(self, m, _json):

        _fname = _json['first_name']
        _lname = None if 'last_name' not in _json.keys() else _json['last_name']
        _email = _json['email']
        #_birthday = _json['birthday']
        _pwd = _json['password']
        _address1 = {} #Empty address on creation of user now. should fix to create with user with if empty leave but enforce later
        _address2 = {}
        _cart = []

        user = m.find_one({'email': _email})
        func.abort_if_exist(user)

        if (_fname or _lname) and _email and _pwd:
            _hashed_pwd = func.hashPassword(_pwd)
            user = {'address1': _address1,'address2': _address2, 'first_name': _fname,
            'last_name': _lname, 'email': _email, 'password': _hashed_pwd, 'cart': _cart}

            return user
        else:
            message = 'Error while adding a user'
            abort(400, message=message)



    def formatRegisterRestaurant(self, m, _json):
           
        _email = _json['email']
        _name = _json['name']
        restaurants = m.find({'email': _email})
        func.abort_if_exist(restaurants)
        restaurants = m.find({'name': _name})
        func.abort_if_exist(restaurants)

        _description = _json['description']
        _pwd = _json['password']
        _tags = _json['tags'] if 'tags' in _json.keys() else None
        
        # All the feilds Not above will be empty on creation.

        if not _name or not _email or not _pwd:
            abort(400, message="The request is not formated correctly name email and restaurant")
        else:
            _hashed_pwd = generate_password_hash(_pwd)
            restaurant = {'name': _name, 'description': _description, 'email': _email, 'password': _hashed_pwd,
                'tags': _tags
                }
            return restaurant

    def formatUpdateUserPassword(self, m, id, _json):
        user = m.find_one({'_id': ObjectId(id)})
        func.abort_if_not_exist(user, "user")
        if 'old_password' not in _json.keys() or 'new_password' not in _json.keys():
            abort(400, message="Not all the parameters were passed")
    
        hashed_old_password = user['password']
        unhashed_old_password =  _json['old_password']
        newPassword = _json['new_password']
        if func.checkPassword(hashed_old_password, unhashed_old_password):
            newPassword = func.hashPassword(newPassword)
            return newPassword
        else:
            abort(400, "Old password doesn't match")

    def formatUpdateUserEmail(self, m, id, _json):
        user = m.find_one({'_id': ObjectId(id)})
        func.abort_if_not_exist(user, "user")
        if 'old_email' not in _json.keys() or 'new_email' not in _json.keys():
            abort(400, message="Not all the parameters were passed")
    
        email = user['email']
        old_email =  _json['old_email']
        new_email = _json['new_email']
        if email.lower() == old_email.lower(): 
            return new_email
        else:
            abort(400, message="Old Email doesn't match")

class UserFunctions():
    def formatUpdateUser(self, _json):
    
        if 'first_name' not in _json.keys():
            abort(400, message="First name must be included")
        if "password" in _json.keys():
            _json.pop('password')
        if "email" in _json.keys():
            _json.pop('email')
        _fname = _json['first_name']
        _lname = None if 'last_name' not in _json.keys() else _json['last_name']
        user = {'first_name': _fname, 'last_name': _lname}
        return user
        





class  RestaurantFunctions():
    def formatAddRestaurant(self, m, _json):
        if 'email' not in _json.keys() or 'name' not in _json.keys() or 'password' not in _json.keys():
            abort(400, message='The request is not formated correctly')
        _email = _json['email']
        restaurants = m.find_one({'email': _email})
        func.abort_if_exist(restaurants)
        #abort if name exists
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
            if 'email' not in _json.keys() or 'name' not in _json.keys():
                abort(400, message='The request is not formated correctly')

            # Restaurant email and password must be specially checked before updating thus new resource
            _email = _json['email']
            _name = _json['name']
            _description = _json['description']
            
            _tags = _json['tags']
            
            # All the fields not here Will be updated on later

            if not _name or not _email:
                abort(400, message="The request is not formated correctly name email and restaurant")
            else:
                restaurant = {'name': _name, 'description': _description, 'email': _email,
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
        if 'meals' not in restaurant.keys():
            restaurant['meals'] = []
        for i in restaurant['meals']:
            if i['name'] == _json['meal']['name']:
                abort(404, message="A restaurant with this name already exists")
        
        operation = {'$push': {"meals": _json['meal']}}

        return operation

    def formatFeedback(self, _json):

        feedback = []
        # add Checks for rating
        for i in _json:
            # Before adding feedback check if user exists and has placed an order from this restaurant
            # For meal feedback add check that the user has an order with this meal
            _user = ObjectId(i['user'])
            _rating = i['rating']
            _comment = i['comment']
            _date = datetime.now()
            feedback.append({'user':_user, 'rating':_rating, 'comment':_comment, 'date':_date})

        return feedback

    def updateRestaurantFeedback(self, _json):
        # json feedback is an array
        if "feedbacks" not in _json.keys():
            abort(400, message="The request feedback is not formated correctly")

        _feedback = self.formatFeedback(_json['feedbacks'])
        operation = {'$addToSet': {"feedbacks":{'$each': _feedback}}}
        return operation

    def updateMealFeedback(self, meal_index, _json):
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
            "Restaurant.password":0, "Restaurant.description":0, "Restaurant.address":0}}
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

    def formatDetailedOrder(self, m, id):
        order_detailed = self.getOrderDetails(m, id)

        if order_detailed[0]['meal'] is not None:
            mIndex = order_detailed[0]['meal']['index']
            mQuantity = order_detailed[0]['meal']['quantity']
            mPortion = order_detailed[0]['meal']['portion']
            ordered_meal = self.getOrderedMeal(order_detailed, mIndex)
            order_detailed[0]['restaurant_name'] = order_detailed[0]["Restaurant"][0]['name']
            order_detailed[0]['meal'] = ordered_meal
            order_detailed[0]['meal_quantity'] = mQuantity

            if mPortion.lower() != "small" and mPortion.lower() != "medium" and mPortion.lower() != "large":
                abort(400, message="portion must be either small, medium or large")
            
            order_detailed[0]['meal_portion'] = mPortion
            oMPrice = ordered_meal['portions'][mPortion]
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
        order_detailed[0]['meal'].pop('portions')
        
        return order_detailed

    def getOrderEntityDetails(self, m, entity, id):
        operation = m.aggregate([{'$match': {entity: ObjectId(id)}},
            {'$lookup':{
                'from': "restaurant",
                'localField': "restaurant",
                'foreignField': "_id",
                'as': "Restaurant"
            }
            },{'$project':{"Restaurant.meals.feedbacks":0, "Restaurant.imgs":0,
            "Restaurant.availability":0, "Restaurant.feedback":0, "Restaurant.tags":0,
            "Restaurant.password":0, "Restaurant.description":0, "Restaurant.address":0}}
        ])
        return list(operation)