#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-python-client.
# https://github.com/akolpakov/paynova-api-python-client

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from unittest import TestCase as PythonTestCase


class TestCase(PythonTestCase):
    MERCHANT_ID = 'test_merchant_id'
    MERCHANT_PASSWORD = 'test_merchant_password'
    ORDER_ID = '70bf60e7-cc9b-4321-bb32-a449010f45a5'
    ORDER_SESSION_ID = 'test-session-id'
    ORDER_URL = 'http://test.com'
