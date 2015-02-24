#Paynova API Python Client

This is an overview of the Paynova API Python Client using [Paynova REST API][] (Aero). More in-depth information can be found in the [Wiki][].
[Paynova REST API]: http://docs.paynova.com/display/API/Paynova+API+Home
[Wiki]: https://github.com/Paynova/paynova-api-php-client/wiki

# Installation
```
pip install paynova-api-python-client
```

# Usage
Create Paynova client:
```python
from paynova_api_python_client import Paynova
client = Paynova('<MERCHANT ID>', '<API Password>')
```

Call service
```python
response = client.create_order({
    'orderNumber': '1234',
    'currencyCode': 'EUR',
    'totalAmount': 10
})
```
See [create simple order example](./examples/create_simple_order.py)

### Paynova requester settings
* **live** - If live = True live endpoint will be used

### Errors
If Paynova return an error **PaynovaException** will be raised
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
To run tests:
```
make tests
```

# License
[MIT licence](./LICENSE)