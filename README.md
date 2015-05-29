#Paynova API Python Client

This is an overview of the Paynova API Python Client using [Paynova REST API](http://docs.paynova.com/display/API/Paynova+API+Home) (Aero). More in-depth information can be found in the [Wiki](https://github.com/Paynova/paynova-api-php-client/wiki).

For Django, see [django-paynova](https://github.com/akolpakov/django-paynova) package

# Installation
```
pip install paynova-api-python-client
```
Python 2.6, 2.7, 3.3, 3.4, PyPy are supported

# Usage
Create Paynova client:
```python
from paynova_api_python_client import Paynova
client = Paynova('<MERCHANT ID>', '<API Password>')
```

Call service
```python
response = client.create_order({
    'orderNumber': 'order-id-0001',
    'currencyCode': 'EUR',
    'totalAmount': 10
})
```

### Examples
* [Create simple order](./examples/create_simple_order.py)
* [Create detailed order](./examples/create_detailed_order.py)
* [Initital payment](./examples/initial_payment.py)

### For live version
```python
client = Paynova('<MERCHANT ID>', '<API Password>', live=True)
```

### Errors
If Paynova return an error, **PaynovaException** will be raised
```python
from paynova_api_python_client import PaynovaException

try:
    response = client.create_order()
except PaynovaException as e:
    # process exception
    # e.errorNumber, e.statusKey, e.statusMessage, e.errors
    pass
```

# Tests
At first make sure that you are in virtualenv.

Install all dependencies:
```
make setup
```
To run test:
```
make tests
```

# License
[MIT licence](./LICENSE)
