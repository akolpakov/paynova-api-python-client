#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-python-client.
# https://github.com/akolpakov/paynova-api-python-client

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from .exceptions import PaynovaException

import requests
import json
import re
import logging

log = logging.getLogger(__name__)


class Paynova(object):
    """
        Paynova API requester
        Docs: http://docs.paynova.com/display/API/Paynova+API+Home
    """

    def __init__(self, username, password, live=False, endpoint=None):
        """
            If :debug = True - test endpoint will be used
            :endpoint - custom endpoint
        """
        self.username = username
        self.password = password
        self.live = live
        self.endpoint = endpoint or self.default_endpoint()

    def get_url(self, resource, params=None):
        """
            Generate url for request
        """

        # replace placeholders

        pattern = r'\{(.+?)\}'

        resource = re.sub(pattern, lambda t: str(params.get(t.group(1), '')), resource)

        # build url

        parts = (self.endpoint, '/api/', resource)
        return '/'.join(map(lambda x: str(x).strip('/'), parts))

    def default_endpoint(self):
        """
            Live or sandbox endpoint
        """
        if self.live:
            return 'https://paygate.paynova.com'
        else:
            return 'https://testpaygate.paynova.com'

    def request(self, method, resource, params=None):
        """
            Make request to the server and parse response
        """

        url = self.get_url(resource, params)

        # headers

        headers = {
            'Content-Type': 'application/json'
        }

        auth = requests.auth.HTTPBasicAuth(self.username, self.password)

        # request

        log.info('Request to %s. Data: %s' % (url, params))

        response = requests.request(method, url, data=json.dumps(params), headers=headers, auth=auth)
        response.raise_for_status()

        # response

        log.info('Response from %s: %s' % (url, response.text))
        content = response.json()

        self.parse_status(content.get('status'))

        return content

    @staticmethod
    def parse_status(status):
        if status and not status.get('isSuccess', False):
            raise PaynovaException(status)

    def create_order(self, params):
        """
            Create order
            Docs: http://docs.paynova.com/display/API/Create+Order
        """
        return self.request('POST', 'orders/create', params)

    def initialize_payment(self, params):
        """
            Initialize Payment
            Docs: http://docs.paynova.com/display/API/Initialize+Payment
        """
        return self.request('POST', 'orders/{orderId}/initializePayment', params)

    def finalize_authorization(self, params):
        """
            Finalize Authorization
            Docs: http://docs.paynova.com/display/API/Finalize+Authorization
        """
        return self.request('POST', 'transactions/{transactionId}/finalize/{totalAmount}', params)

    def annul_authorization(self, params):
        """
            Annul Authorization
            Docs: http://docs.paynova.com/display/API/Annul+Authorization
        """
        return self.request('POST', 'transactions/{transactionId}/annul/{totalAmount}', params)

    def refund_payment(self, params):
        """
            Refund Payment
            Docs: http://docs.paynova.com/display/API/Refund+Payment
        """
        return self.request('POST', 'transactions/{transactionId}/refund/{totalAmount}', params)

    def get_customer_profile(self, params):
        """
            Get Customer Profile
            Docs: http://docs.paynova.com/display/API/Get+Customer+Profile
        """
        return self.request('GET', 'customerprofiles/{profileId}', params)

    def remove_customer_profile(self, params):
        """
            Remove Customer Profile
            Docs: http://docs.paynova.com/display/API/Remove+Customer+Profile
        """
        return self.request('DELETE', 'customerprofiles/{profileId}', params)

    def remove_customer_profile_card(self, params):
        """
            Remove Customer Profile Card
            Docs: http://docs.paynova.com/display/API/Remove+Customer+Profile+Card
        """
        return self.request('DELETE', 'customerprofiles/{profileId}/cards/{cardId}', params)