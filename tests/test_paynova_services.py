#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-python-client.
# https://github.com/akolpakov/paynova-api-python-client

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from preggy import expect

from paynova_api_python_client import Paynova, PaynovaException
from tests.base import TestCase
from httmock import all_requests, HTTMock
from requests.exceptions import HTTPError

import sys

_ver = sys.version_info


@all_requests
def paynova_mock(url, request):
    content = None

    def sucecss(content):
        if not content:
            content = {}

        content['status'] = {
            'isSuccess': True,
            'errorNumber': 0,
            'statusKey': 'SUCCESS',
        }

        return {'status_code': 200, 'content': content}

    # create order

    if url[2] == '/api/orders/create':
        return sucecss({
            'orderId': TestCase.ORDER_ID
        })

    # init payment

    elif url[2] == '/api/orders/0001/initializePayment':
        return sucecss({
            'sessionId': TestCase.ORDER_SESSION_ID,
            'url': TestCase.ORDER_URL
        })

    # initialize authorization

    elif url[2] == '/api/transactions/0001/finalize/100':
        return sucecss({
            'canFinalizeAgain': True,
            'amountRemainingForFinalize': 50
        })

    return {'status_code': 404}


class PaynovaServicesTestCase(TestCase):
    def setUp(self):
        self.paynova = Paynova(TestCase.MERCHANT_ID, TestCase.MERCHANT_PASSWORD)

    def tearDown(self):
        pass

    def test_create_order(self):
        with HTTMock(paynova_mock):
            params = {
                'orderNumber': '0001'
            }
            response = self.paynova.create_order(params)
            expect(response).not_to_be_null()
            expect(response.get('orderId')).to_equal(TestCase.ORDER_ID)

    def test_initial_payment(self):
        with HTTMock(paynova_mock):
            params = {
                'orderId': '0001'
            }
            response = self.paynova.initialize_payment(params)
            expect(response).not_to_be_null()
            expect(response.get('sessionId')).to_equal(TestCase.ORDER_SESSION_ID)
            expect(response.get('url')).to_equal(TestCase.ORDER_URL)

    def test_finalize_authorization(self):
        with HTTMock(paynova_mock):
            params = {
                'transactionId': '0001',
                'totalAmount': 100
            }
            response = self.paynova.finalize_authorization(params)
            expect(response).not_to_be_null()
            expect(response.get('canFinalizeAgain')).to_be_true()
            expect(response.get('amountRemainingForFinalize')).to_equal(50)

