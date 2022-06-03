def addDrinks(_json):
    # A drink comes in as an object. added one at a time
    operation = {'$addToSet': {"drinks":{'$each': [_json['drinks']]}}}
    return operation

def updateDrinks(_json):
    # A drink comes in as an object.
    operation = {'$set': {"drinks.$[elem]":_json['drinks']}}
    arrayFilters = [{"elem.name": {'$eq':_json['drinks']['name']}}]
    return operation, arrayFilters