""" Third-party APIs and Services """
import logging
import requests

from urllib.parse import urlencode

class BaseAPI(object):
    """
    Serves as an interface to the third-party APIs used in this project.
    """
    def __init__(self, base, key_name, key_value):
        """
        Initialize a simple API interface, with given parameters.

        Params
        ------
        base: str
            The base URL
        key_name: str
            Authentication key title (e.g. "API_KEY" or "API_SECRET")
        key_value: str
            Authentication key value
        """
        self.base = base
        self.key_name = key_name
        self.key_value = key_value

    def _get_endpoint(self, endpoint='', params=''):
        """
        Gets the full location for the specified endpoint.

        Params
        ------
        endpoint: str
            Optional. The target endpoint
        params: str
            Optional. Query string to be passed with endpoint
        """
        return f"{self.base}{endpoint}?{params}&{self.key_name}={self.key_value}"

    def _query_endpoint(self, endpoint='', params=''):
        """
        Perform a GET call on a specified resource.

        Params
        ------
        endpoint: str
            Optional. The target endpoint
        params: dict
            Optional. A mapping of parameters to be encoded with URL
        """
        url = self._get_endpoint(endpoint, urlencode(params, safe=','))
        data = None
        try:
            r = requests.get(url)
            data = r.json()
        except requests.exceptions.RequestException as e:
            logging.error(str(e))

        return data