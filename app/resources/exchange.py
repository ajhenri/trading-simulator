from flask import request
from flask_restplus import Namespace, Resource, fields

from app.resources.base_resource import BaseResource
from app.services.third_party.wtd import WorldTradingData

exchange_ns = Namespace('exchange', description='Exchange API Functions')

@exchange_ns.doc()
@exchange_ns.route('/')
class ExchangeResource(BaseResource):
    def get(self):
        """
        Retrieve summaries and up-to-date price information for specified list of stocks.
        """
        stock_list = request.args.getlist("stock")
        results = []
        if len(stock_list) > 0:
            stocks = WorldTradingData().get_stocks(stock_list)
            results = stocks['data']
        return self.success_response(results)

@exchange_ns.doc()
@exchange_ns.route('/search/<ticker>')
class ExchangeSearchResource(BaseResource):
    def get(self, ticker):
        """
        Search for stock with ticker specified.

        Params
        ------
        ticker : str
            The stock ticker (e.g. TSLA, APPL)
        """
        api = WorldTradingData()
        data = api.search(ticker)
        return self.success_response(data['data'])