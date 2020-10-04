import bcrypt
import secrets
import logging

from http import HTTPStatus
from flask import request, Blueprint
from marshmallow import ValidationError
from flask_restful import Api, Resource

from trader.extensions import db
from trader.lib.definitions import ResponseErrors
from trader.resources.base_resource import BaseResource, validate_request_json
from trader.models import User
from trader.schemas import UserVerifySchema, UserSchema, ClientSchema

users_bp = Blueprint('users', __name__)
users = Api(users_bp)

class UserVerifyResource(BaseResource):
    @validate_request_json
    def post(self):
        """
        Checks database for user of given `email` and compares 
        passwords for login verification.
        """
        schema = UserVerifySchema()
        try:
            data = schema.loads(request.get_data())
        except ValidationError as err:
            return self.error_response(err.messages, HTTPStatus.BAD_REQUEST)

        with db.session_scope() as session:
            user = session.query(User).filter_by(email=data['email']).first()
            if not user:
                return self.success_response(result=False)

            password = bcrypt.hashpw(data['password'].encode(), user.salt)
            verify = password == user.password
            return self.success_response(result=verify)
class UserResource(BaseResource):
    def get(self, id):
        """
        Get user information based on user ID.
        Returns an HTTP 404 error if user doesn't exist.

        Params
        ------
        id: int
            The identifier of the user
        """
        with db.session_scope() as session:
            user = session.query(User).filter_by(id=id).first()
            if not user:
                return self.error_response(ResponseErrors.USER_DNE, HTTPStatus.NOT_FOUND)

            schema = UserSchema()
            data = schema.dump(user)
            if user.account:
                data['account_id'] = user.account.id
        return self.success_response(data)
    
    @validate_request_json
    def post(self):
        """
        Creates a new user, and creates a client associated with that user assigned to the default scope.
        """
        schema = UserSchema()
        try:
            data = schema.loads(request.get_data())
        except ValidationError as err:
            return self.error_response(err.messages, HTTPStatus.BAD_REQUEST)
        
        user_id = client_id = None
        try:
            with db.session_scope() as session:
                user = session.query(User).filter_by(email=data['email']).first()
                if user:
                    return self.error_response('User already exists')

                salt = bcrypt.gensalt()
                hashed_pw = bcrypt.hashpw(data['password'].encode(), salt)

                user_input = {
                    'email': data['email'],
                    'password': hashed_pw,
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'salt': salt
                }
                user = User(**user_input)
                session.add(user)
                session.flush()

                if not user.id:
                    logging.debug(user_input)
                    raise Exception('User creation failed')
                user_id = user.id
        except Exception as e:
            logging.debug(str(e))
            return self.error_response(ResponseErrors.DEFAULT)

        return self.success_response(result={'user_id': user_id, 'client_id': client_id}, \
            success=True, status_code=HTTPStatus.CREATED)

users.add_resource(UserResource, '', methods=['POST'])
users.add_resource(UserResource, '/<int:id>', methods=['GET', 'PATCH'], endpoint='users_by_id')
users.add_resource(UserVerifyResource, '/verify', methods=['POST'])