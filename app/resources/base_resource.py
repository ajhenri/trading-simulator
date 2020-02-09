import logging

from functools import wraps
from flask import request, jsonify
from flask_restplus import Resource

from app.lib import errors

class BaseResource(Resource):
    HTTP_OK = 200
    HTTP_CREATED = 201
    HTTP_BAD_REQUEST = 400
    HTTP_NOT_FOUND = 404
    HTTP_METHOD_NOT_ALLOWED = 405
    HTTP_INTERNAL_SERVER_ERROR = 500

    def http_response(self, response, status_code):
        return response, status_code

    def error_response(self, error, status_code=HTTP_INTERNAL_SERVER_ERROR):
        response = {}
        response['error'] = error
        return self.http_response(response, status_code)

    def success_response(self, result={}, success=True, status_code=HTTP_OK):
        response = {}
        response['result'] = result
        response['success'] = success
        return self.http_response(response, status_code)

def validate_request_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        json_data = None
        try:
            json_data = request.get_json()
        except Exception as e:
            response = {'error': errors.INVALID_JSON}
            return response, BaseResource.HTTP_BAD_REQUEST
        return f(*args, **kwargs)
    return decorated