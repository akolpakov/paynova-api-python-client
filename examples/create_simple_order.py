from paynova_api_python_client import Paynova, PaynovaException

import logging
logging.basicConfig(level='DEBUG')

# test client

client = Paynova('<MERCHANT ID>', '<API Password>')

try:
    # create order

    response = client.create_order({
        'orderNumber': '1234',
        'currencyCode': 'EUR',
        'totalAmount': 10
    })

    # get order id from response

    orderId = response.get('orderId')

except PaynovaException as e:
    # process exception
    # e.errorNumber, e.statusKey, e.statusMessage, e.errors
    pass