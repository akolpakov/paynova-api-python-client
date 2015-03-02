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

    # init payment
    # For more information about parameters, see http://docs.paynova.com/display/API/Initialize+Payment

    response = client.initialize_payment({
        'orderId': orderId,
        'totalAmount': 10,
        'paymentChannelId': 1,
        'interfaceOptions': {
            'interfaceId': 5,
            'customerLanguageCode': 'eng',
            'urlRedirectSuccess': 'http://www.merchant-url.com/success',    # Change to your URL
            'urlRedirectCancel': 'http://www.merchant-url.com/cancel',    # Change to your URL
            'urlRedirectPending': 'http://www.merchant-url.com/pending',    # Change to your URL
            'urlCallback': 'http://www.url-where-to-receive-event-hooks.com/',    # Change to your URL
        }
    })

    url = response.get('url')

    # redirect to url

except PaynovaException as e:
    # process exception
    # e.errorNumber, e.statusKey, e.statusMessage, e.errors
    pass