from . import BaseAPI
from flask import current_app

class WorldTradingData(BaseAPI):
    """
    Serves as an interface to the World Trading Data API.
    """
    def __init__(self):
        super().__init__(current_app.config['WTD_API_URL'], 'api_token', 
            current_app.config['WTD_API_KEY'])
    
    def get_stocks(self, tickers):
        """
        Get a list of stocks from WTD.

        Params
        ------
        tickers: list
            The list of tickers to get information for.
        """
        return self._query_endpoint('stock', {
            'symbol': ",".join(tickers),
            'sort_order': 'asc',
            'sort_by': 'symbol'
        })

    def search(self, ticker, page=1):
        """
        Search for specified ticker in WTD.

        Params
        ------
        ticker: str
            The ticker to search for.
        """
        stock_list = self._query_endpoint('stock_search', {
            'search_term': ticker,
            'search_by': 'symbol',
            'stock_exchange': 'NASDAQ,NYSE',
            'page': page
        })

        return stock_list if stock_list else []