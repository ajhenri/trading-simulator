from flask import request, jsonify
from flask_restplus import Resource

class BaseResource(Resource):
    def http_response(self, response, status_code):
        return response, status_code

    def error_response(self, response, status_code=400):
        return self.http_response(response, status_code)

    def success_response(self, response, status_code=200):
        return self.http_response(response, status_code)