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

import base64
import json
import sys

_ver = sys.version_info


@all_requests
def paynova_mock(url, request):
    content = None

    # simple test

    if url[2] == '/api/return/request':
        content = json.loads(request.body)

    # test basic authentication

    elif url[2] == '/api/auth/check':
        auth = request.headers.get('authorization')

        if _ver >= (3, 0):
            username_password = '%s:%s' % (TestCase.MERCHANT_ID, TestCase.MERCHANT_PASSWORD)
            username_password = base64.b64encode(username_password.encode('ascii'))
            auth_string = 'Basic %s' % username_password.decode('ascii')
        else:
            auth_string = 'Basic %s' % base64.b64encode('%s:%s' % (TestCase.MERCHANT_ID, TestCase.MERCHANT_PASSWORD))

        if auth == auth_string:
            content = {'result': 'success'}
        else:
            return {'status_code': 401, 'reason': 'No credentials were provided'}

    # test status

    elif url[2] == '/api/status/error':
        content = {'status': {
            'isSuccess': False,
            'errorNumber': -2,
            'statusKey': 'VALIDATION_ERROR',
            'statusMessage': 'The request contained one or more validation errors. See the errors collection for further details.',
            'errors': [{
                'errorCode': 'Length',
                'fieldName': 'OrderNumber',
                'message': '\'Order Number\' must be between 4 and 50 characters. You entered 0 characters.',
           }]
        }}

    elif url[2] == '/api/status/success':
        content = {'status': {
            'isSuccess': True,
        }}

    return {'status_code': 200, 'content': content}


class PaynovaTestCase(TestCase):
    def setUp(self):
        self.paynova = Paynova(TestCase.MERCHANT_ID, TestCase.MERCHANT_PASSWORD)

    def tearDown(self):
        pass

    def test_init(self):
        expect(self.paynova.username).to_equal(TestCase.MERCHANT_ID)
        expect(self.paynova.password).to_equal(TestCase.MERCHANT_PASSWORD)

    def test_init_endpoint(self):
        paynova = Paynova(TestCase.MERCHANT_ID, TestCase.MERCHANT_PASSWORD)
        expect(paynova.endpoint).to_equal('https://testpaygate.paynova.com')

        paynova = Paynova(TestCase.MERCHANT_ID, TestCase.MERCHANT_PASSWORD, live=True)
        expect(paynova.endpoint).to_equal('https://paygate.paynova.com')

        paynova = Paynova(TestCase.MERCHANT_ID, TestCase.MERCHANT_PASSWORD, endpoint='https://test.com')
        expect(paynova.endpoint).to_equal('https://test.com')

    def test_get_url(self):
        expect(self.paynova.get_url('test/res')).to_equal('https://testpaygate.paynova.com/api/test/res')
        expect(self.paynova.get_url('/test/res')).to_equal('https://testpaygate.paynova.com/api/test/res')
        expect(self.paynova.get_url('/test/res/')).to_equal('https://testpaygate.paynova.com/api/test/res')

    def test_get_url_with_param(self):
        params = {
            'orderId': 123
        }
        expect(self.paynova.get_url('test/{orderId}', params=params)).to_equal('https://testpaygate.paynova.com/api/test/123')
        expect(self.paynova.get_url('test/{noParam}', params=params)).to_equal('https://testpaygate.paynova.com/api/test')

    def test_request(self):
        with HTTMock(paynova_mock):
            params = {
                'test1': 1,
                'test2': 2
            }
            response = self.paynova.request('POST', 'return/request', params)
            expect(response).to_equal(params)

    def test_request_auth(self):
        with HTTMock(paynova_mock):
            response = self.paynova.request('POST', 'auth/check')
            expect(response.get('result')).to_equal('success')

    def test_request_auth_fail(self):
        with HTTMock(paynova_mock):
            paynova = Paynova(TestCase.MERCHANT_ID, 'wrong_password')
            with expect.error_to_happen(HTTPError):
                paynova.request('POST', 'auth/check')

    def test_status(self):
        with HTTMock(paynova_mock):
            with expect.error_to_happen(PaynovaException):
                self.paynova.request('POST', 'status/error')

            response = self.paynova.request('POST', 'status/success')
            expect(response).not_to_be_null()
