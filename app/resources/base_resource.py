from flask import request, jsonify
from flask_restplus import Resource

class BaseResource(Resource):
    HTTP_OK = 200
    HTTP_CREATED = 201
    HTTP_BAD_REQUEST = 400
    HTTP_NOT_FOUND = 404
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