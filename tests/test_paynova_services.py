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

    def success(content=None):
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
        return success({
            'orderId': TestCase.ORDER_ID
        })

    # init payment

    elif url[2] == '/api/orders/0001/initializePayment':
        return success({
            'sessionId': TestCase.ORDER_SESSION_ID,
            'url': TestCase.ORDER_URL
        })

    # initialize authorization

    elif url[2] == '/api/transactions/0001/finalize/100':
        return success({
            'canFinalizeAgain': True,
            'amountRemainingForFinalize': 50
        })

    # annul authorization

    elif url[2] == '/api/transactions/0001/annul/100':
        return success()

    # refund

    elif url[2] == '/api/transactions/0001/refund/100':
        return success({
            'transactionId': '0001',
            'batchId': 'batch'
        })

    # get customer profile

    elif url[2] == '/api/customerprofiles/1':
        return success({
            'profileId': '1'
        })

    # remove customer profile

    elif url[2] == '/api/customerprofiles/1' and request.method == 'DELETE':
        return success()

    # remove customer profile card

    elif url[2] == '/api/customerprofiles/1/cards/1' and request.method == 'DELETE':
        return success()

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

    def test_annul_authorization(self):
        with HTTMock(paynova_mock):
            params = {
                'transactionId': '0001',
                'totalAmount': 100
            }
            response = self.paynova.annul_authorization(params)
            expect(response).not_to_be_null()

    def test_refund_payment(self):
        with HTTMock(paynova_mock):
            params = {
                'transactionId': '0001',
                'totalAmount': 100
            }
            response = self.paynova.refund_payment(params)
            expect(response).not_to_be_null()
            expect(response.get('transactionId')).to_equal('0001')
            expect(response.get('batchId')).to_equal('batch')

    def test_get_customer_profile(self):
        with HTTMock(paynova_mock):
            params = {
                'profileId': '1'
            }
            response = self.paynova.get_customer_profile(params)
            expect(response).not_to_be_null()
            expect(response.get('profileId')).to_equal('1')

    def test_remove_customer_profile(self):
        with HTTMock(paynova_mock):
            params = {
                'profileId': '1'
            }
            response = self.paynova.remove_customer_profile(params)
            expect(response).not_to_be_null()

    def test_remove_customer_profile_card(self):
        with HTTMock(paynova_mock):
            params = {
                'profileId': '1',
                'cardId': '1'
            }
            response = self.paynova.remove_customer_profile_card(params)
            expect(response).not_to_be_null()