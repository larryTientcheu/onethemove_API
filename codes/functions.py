from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import abort

class Functions:
    def __init__(self) -> None:
        pass

    def hashPassword(self, password):
        hashed = generate_password_hash(password)
        return hashed

    # takes db hashed password, actual form passord
    def checkPassword(self, hashed, password):
        result = check_password_hash(hashed, password)
        return result

    def abort_if_exist(self, resource):
        if resource is not None:
            abort(409, message="This resource already exists...")


    def abort_if_not_exist(self, resource, r):
        if resource is None:
            abort(404, message="This {} doesn't exist".format(r))
    