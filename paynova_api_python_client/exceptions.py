#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-python-client.
# https://github.com/akolpakov/paynova-api-python-client

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>


class PaynovaException(Exception):
    """
        Paynova Exception based on status in response
        Docs: http://docs.paynova.com/display/API/Paynova+API+Home
    """
    def __init__(self, status):
        self.errorNumber = status.get('errorNumber')
        self.statusKey = status.get('statusKey')
        self.statusMessage = status.get('statusMessage')
        self.errors = status.get('errors')
        self.exceptionDetails = status.get('exceptionDetails')