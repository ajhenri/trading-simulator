import json
import math

from datetime import datetime, timedelta
from flask import request, Blueprint
from flask_restful import Api, Resource
from trader.resources.base_resource import BaseResource

exchange_bp = Blueprint('exchange', __name__)
exchange = Api(exchange_bp)

class ExchangeResource(BaseResource):
    def get(self):
        """
        Retrieve summaries and up-to-date price information for specified list of stocks.
        """
        stock_list = request.args.getlist("stock")
        results = []
        if len(stock_list) > 0:
            response = self.iex_api.get_stock_data(stock_list)
        return self.success_response(response)

class ExchangeSearchResource(BaseResource):
    def get(self, symbol):
        """
        Search for stock with symbol specified.

        Params
        ------
        symbol : str
        """
        response = self.iex_api.search_symbol(symbol)
        return self.success_response(response)

exchange.add_resource(ExchangeResource, '', methods=['GET'])
exchange.add_resource(ExchangeSearchResource, '/search/<string:symbol>', methods=['GET'])