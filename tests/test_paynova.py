#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-python-client.
# https://github.com/akolpakov/paynova-api-python-client

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from preggy import expect

from paynova_api_python_client import Paynova
from tests.base import TestCase
from httmock import urlmatch, HTTMock


@urlmatch(netloc=r'(.*\.)?paynova\.com$')
def paynova_mock(url, request):
    response = None

    if url[2] == '/api/return/request' and request.method == 'POST':
        response = request.body

    return response


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
        expect(paynova.endpoint).to_equal('https://paygate.paynova.com')

        paynova = Paynova(TestCase.MERCHANT_ID, TestCase.MERCHANT_PASSWORD, debug=True)
        expect(paynova.endpoint).to_equal('https://testpaygate.paynova.com')

        paynova = Paynova(TestCase.MERCHANT_ID, TestCase.MERCHANT_PASSWORD, endpoint='https://test.com')
        expect(paynova.endpoint).to_equal('https://test.com')

    def test_get_url(self):
        expect(self.paynova.get_url('test/res')).to_equal('https://paygate.paynova.com/api/test/res')
        expect(self.paynova.get_url('/test/res')).to_equal('https://paygate.paynova.com/api/test/res')
        expect(self.paynova.get_url('/test/res/')).to_equal('https://paygate.paynova.com/api/test/res')

    def test_request(self):
        with HTTMock(paynova_mock):
            params = {
                'test1': 1,
                'test2': 2
            }
            response = self.paynova.request('POST', 'return/request', params)
            expect(response).to_equal(params)
