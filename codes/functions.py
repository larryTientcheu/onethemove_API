from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import abort

class Functions:
    def __init__(self) -> None:
        pass

    def hashPassword(self, password):
        hashed = generate_password_hash(password)
        return hashed

    
    def checkPassword(self, hashed, password):
        result = check_password_hash(hashed, password)
        return result

    # def abort_if_not_exist(self, users):
    #     if users is None:
    #         abort(404, message="No user exists with this email address")

    # String dump check
    # def abort_if_exist(self, email, users):
    #     if email in users:
    #         abort(409, message="User already exists with that email ID...")

    def abort_if_exist(self, users):
        if users is not None:
            abort(409, message="User already exists with that email ID...")