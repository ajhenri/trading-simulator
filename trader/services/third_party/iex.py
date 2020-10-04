import requests
import logging

from flask import current_app as app

class IEXApi:

    def __init__(self):
        if app.config['ENV'] == 'prod':
            self.base_url = 'https://cloud.iexapis.com/stable'
            self.token = app.config['IEX_SECRET_TOKEN']
        else:
            self.base_url = 'https://sandbox.iexapis.com/stable'
            self.token = app.config['IEX_SB_SECRET_TOKEN']

    def search_symbol(self, symbol):
        url = f"{self.base_url}/search/{symbol}?token={self.token}"
        try:
            res = requests.get(url)
            data = res.json()
        except Exception as e:
            logging.error({'exception': str(e), 'res': res.content})
            return False
        
        return data

    def get_stock_data(self, symbols):
        symbols_str = ','.join(symbols)
        url = f"{self.base_url}/stock/market/batch?symbols={symbols_str}&types=quote,news,chart&range=1m&last=5&token={self.token}"
        try:
            res = requests.get(url)
            data = res.json()
        except Exception as e:
            logging.error({'exception': str(e), 'res': res.content})
            return False

        return data