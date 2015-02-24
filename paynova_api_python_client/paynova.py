from urlparse import urljoin

import requests
import json
import logging

log = logging.getLogger(__name__)


class Paynova(object):
    """
        Paynova API requester
        Docs: http://docs.paynova.com/display/API/Paynova+API+Home
    """

    def __init__(self, username, password, debug=False, endpoint=None):
        """
            If :debug = True - test endpoint will be used
            :endpoint - custom endpoint
        """
        self.username = username
        self.password = password
        self.debug = debug
        self.endpoint = endpoint or self.default_endpoint()

    def get_url(self, resource, params=None):
        """
            Generate url for request
        """

        parts = (self.endpoint, '/api/', resource)

        return '/'.join(map(lambda x: str(x).strip('/'), parts))

    def default_endpoint(self):
        """
            Live or sandbox endpoint
        """
        if self.debug:
            return 'https://testpaygate.paynova.com'
        else:
            return 'https://paygate.paynova.com'

    def request(self, method, resource, params):
        """
            Make request to the server and parse response
        """

        url = self.get_url(resource, params)

        # headers

        headers = {
            'Content-Type': 'application/json'
        }

        # request

        log.info('Request to %s. Data: %s' % (url, params))

        response = requests.request(method, url, data=json.dumps(params), headers=headers)
        response.raise_for_status()

        # response

        log.info('Response from %s: %s' % (url, response.text))
        content = response.json()

        return content

    # def create_order(self, params):
    #     """
    #         Create order
    #         Docs: http://docs.paynova.com/display/API/Create+Order
    #     """
    #     self.request('POST', 'orders/create', params)