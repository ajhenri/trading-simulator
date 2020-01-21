from flask import request, jsonify
from flask_restplus import Resource
class BaseResource(Resource):
    DEFAULT_ERROR_MESSAGE = 'An unexpected error occurred while processing this request'

    def http_response(self, response, status_code):
        return response, status_code

    def error_response(self, error, status_code=400):
        response = {}
        response['error'] = error
        return self.http_response(response, status_code)

    def success_response(self, result={}, success=True, status_code=200):
        response = {}
        response['result'] = result
        response['success'] = success
        return self.http_response(response, status_code)