from . import BaseAPI
from flask import current_app as app

class WorldTradingData(BaseAPI):
    """
    Serves as an interface to the World Trading Data API.
    """
    def __init__(self):
        super().__init__(app.config['WTD_API_URL'], 'api_token', 
            app.config['WTD_API_KEY'])
    
    def get_stocks(self, symbols):
        """
        Get a list of stocks from WTD.

        Params
        ------
        symbols: list
            The list of symbols to get information for.
        """
        return self._query_endpoint('stock', {
            'symbol': ",".join(symbols),
            'sort_order': 'asc',
            'sort_by': 'symbol'
        })

    def search(self, symbol, page=1):
        """
        Search for specified symbol in WTD.

        Params
        ------
        symbol: str
            The symbol to search for.
        """
        stock_list = self._query_endpoint('stock_search', {
            'search_term': symbol,
            'search_by': 'symbol',
            'stock_exchange': 'NASDAQ,NYSE',
            'page': page
        })

        return stock_list if stock_list else []

    def historical_data(self, symbol, date_from, date_to):
        """
        Get historical price data for a specified stock symbol.

        Params
        ------
        symbol: str
            
        """
        data = self._query_endpoint('history', {
            'symbol': symbol,
            'date_to': date_to,
            'date_from': date_from
        })

        return data['history']