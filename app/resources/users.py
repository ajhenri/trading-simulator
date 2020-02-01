import bcrypt
import secrets
import logging

from flask import request
from marshmallow import ValidationError
from flask_restplus import Namespace, Resource, fields

from app.database import session_scope
from app.resources.base_resource import BaseResource
from app.models import User, OauthClient, OauthClientScope
from app.schemas import UserVerifySchema, UserSchema, ClientSchema

users_ns = Namespace('users', description='User API Functions')

@users_ns.doc()
class UserVerifyResource(BaseResource):
    """
    Verifying Users
    """
    def post(self):
        """
        Checks database for user of given `username` and compares 
        passwords for login verification.
        """
        try:
            schema = UserVerifySchema()
            data = schema.loads(request.get_data())
            with session_scope() as session:
                user = session.query(User).filter_by(username=data['username']).first()
                if not user:
                    return self.success_response(result=False)

                password = bcrypt.hashpw(data['password'].encode(), user.salt)
                verify = password == user.password
                return self.success_response(result=verify)
        except ValidationError as err:
            logging.debug(err)
            return self.error_response(err.messages)
        except Exception as err:
            logging.debug(str(err))
            return self.error_response(self.DEFAULT_ERROR_MESSAGE)

@users_ns.doc()
class UserResource(BaseResource):
    """
    Resource for API Users
    """
    def get(self, id):
        """
        Get user information based on user ID.
        Returns an HTTP 404 error if user doesn't exist.

        Params
        ------
        id: int
            The identifier of the user
        """
        with session_scope() as session:
            user = session.query(User).filter_by(id=id).first()
            if not user:
                return self.error_response('User does not exist', 404)

            schema = UserSchema()
            try:
                data = schema.dump(user)
            except ValidationError as err:
                logging.debug(err)
                return self.error_response(err.messages)
        return self.success_response(data)
    
    def post(self):
        """
        Creates a new user, and creates a client associated with that user assigned to the default scope.
        """
        schema = UserSchema()
        try:
            data = schema.loads(request.get_data())
        except ValidationError as err:
            logging.debug(err)
            return self.error_response(err.messages)
        except Exception as err:
            logging.debug(str(err))
            return self.error_response('Error parsing JSON request')
        
        user_id = client_id = None
        try:
            with session_scope() as session:
                user = session.query(User).filter_by(username=data['username']).first()
                if user:
                    return self.error_response('User already exists')

                salt = bcrypt.gensalt()
                hashed_pw = bcrypt.hashpw(data['password'].encode(), salt)

                user_input = {
                    'username': data['username'],
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

                client_id = secrets.token_hex(16)
                client_secret = secrets.token_hex(32)
                
                # For now, client name will just be user's full name.
                client_name = f"{data['first_name']} {data['last_name']}"
                client_input = {
                    'client_id': client_id,
                    'client_name': client_name,
                    'client_secret': client_secret,
                    'redirect_uri': 'http://0.0.0.0:5050/auth/callback',
                    'user_id': user.id
                }
                client = OauthClient(**client_input)
                session.add(client)
                session.flush()
                
                if not client.client_id:
                    logging.debug(client_input)
                    raise Exception('Client creation failed')
                
                client_scope = OauthClientScope(
                    client_id=client.client_id,
                    scope_id=1
                )
                session.add(client_scope)
                session.flush()

                if not client_scope.id:
                    raise Exception('Client scope creation failed')
        except Exception as e:
            logging.debug(str(e))
            return self.error_response(self.DEFAULT_ERROR_MESSAGE)

        return self.success_response(result={'user_id': user_id, 'client_id': client_id}, \
            success=True, status_code=201)

users_ns.add_resource(UserResource, '', methods=['POST'])
users_ns.add_resource(UserResource, '/<id>', methods=['GET', 'PATCH'])
users_ns.add_resource(UserVerifyResource, '/verify', methods=['POST'])