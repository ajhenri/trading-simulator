from flask_restplus import Namespace, Resource, fields

exchange_ns = Namespace('exchange', description='Exchange API Functions')

@exchange_ns.doc()
@exchange_ns.route('/')
class ExchangeResource(Resource):
    def get(self, ticker_list):
        return {}

@exchange_ns.doc()
@exchange_ns.route('/search/<ticker>')
class ExchangeSearchResource(Resource):
    def get(self, ticker):
        return {}

@exchange_ns.doc()
@exchange_ns.route('/news', '/<ticker>/news')
class ExchangeNewsResource(Resource):
    def get(self, ticker=None):
        return {}