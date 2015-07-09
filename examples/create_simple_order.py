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
        'totalAmount': 10
    })

    # get order id from response

    orderId = response.get('orderId')

except PaynovaException as e:
    # process exception
    # e.errorNumber, e.statusKey, e.statusMessage, e.errors
    pass
