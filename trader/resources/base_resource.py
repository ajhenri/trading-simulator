import logging

from http import HTTPStatus
from functools import wraps
from flask import request, jsonify
from flask_restful import Resource

from trader.lib.definitions import ResponseErrors
from trader.services.third_party.iex import IEXApi

class BaseResource(Resource):
    def __init__(self):
        self.iex_api = IEXApi()

    def http_response(self, response, status_code):
        return response, status_code

    def error_response(self, error, status_code):
        response = {}
        response['error'] = error
        return self.http_response(response, status_code)

    def success_response(self, result={}, success=True, status_code=HTTPStatus.OK):
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
            response = {'error': ResponseErrors.INVALID_JSON}
            return response, HTTPStatus.BAD_REQUEST
        return f(*args, **kwargs)
    return decorated