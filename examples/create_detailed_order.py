from paynova_api_python_client import Paynova, PaynovaException

import logging
logging.basicConfig(level='DEBUG')

# test client

client = Paynova('<MERCHANT ID>', '<API Password>')

try:
    # create order
    # For more information about parameters, see http://docs.paynova.com/display/API/Create+Order

    response = client.create_order({
        'orderNumber': 'order-id-0001',
        'currencyCode': 'EUR',
        'totalAmount': 10,
        'orderDescription': 'This is a test order',
        'salesChannel': 'My channel',
        'salesLocationId': 'Test Shop',
        'customer': {
            'customerId': '0001',
            'emailAddress': 'test@test.com',
            'name': {
                'companyName': None,
                'title': 'Mr.',
                'firstName': 'John',
                'middleNames': None,
                'lastName': 'Snow',
                'suffix': 'Sr.'
            },
            'homeTelephone': '+1234567890',
            'workTelephone': None,
            'mobileTelephone': None,
        },
        'billTo': None,
        'shipTo': None,
        'lineItems': [
            {
                'id': '0001',
                'articleNumber': 'item-0001',
                'name': 'Product',
                'description': 'Our test product',
                'quantity': 1,
                'unitMeasure': 'meters',
                'unitAmountExcludingTax': 10,
                'taxPercent': 0,
                'totalLineTaxAmount': 0,
                'totalLineAmount': 10
            }
        ]
    })

    # get order id from response

    orderId = response.get('orderId')

except PaynovaException as e:
    # process exception
    # e.errorNumber, e.statusKey, e.statusMessage, e.errors
    pass