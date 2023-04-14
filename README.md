# Lambda Runtimes

Python library for getting a list of all Lambda runtimes from AWS's documentation page, and interacting with it.

## Usage

You can install the `lambda-runtimes` package from PyPI with pip:

```pip3 install lambda-runtimes```

or clone this repository and install the requirements with `pip3 install -r requirements.txt`

### Basic Usage

The LambdaRuntimes library implements a list of LambdaRuntimes fetched from the AWS documentation website. Internally, it is just a list of results parsed from the tables on the Lambda runtimes page with some helper functions to make working with them easier.

Import the library at the top of your python file and create an instance of the `LambdaRuntimes` class. This fetches a list of the runtimes from the AWS docs page.

```python
from lambdaruntimes import LambdaRuntimes
runtimes = LambdaRuntimes()
```

You can optionally specify another location for the source docs page if you have a cache or proxy.

```python
from lambdaruntimes import LambdaRuntimes
runtimes = LambdaRuntimes(lambda_runtime_docs_url="http://localhost:8000/lambda-runtimes.html")
```

#### Iterating Over Runtimes

The `LambdaRuntimes` class is a valid iterator, so you can loop over all runtimes using normal Python flow control tools.

```python
from lambdaruntimes import LambdaRuntimes
runtimes = LambdaRuntimes()
for runtime in runtimes:
    print(runtime)
```

You can also directly access the `runtimes` property of the instance, and iterate over it instead.

#### Getting a Single Runtime

You can query for a runtime by its identifier using the `get_runtime()` function.

```python
runtimes.get_runtime("nodejs")
>>> LambdaRuntime(name='Node.js 0.10', identifier='nodejs', sdk=None, os='Amazon Linux', arch=None, deprecation_phase_1=datetime.datetime(2016, 10, 31, 0, 0), deprecation_phase_2=datetime.datetime(2016, 10, 31, 0, 0), runtime_is_expiring=True, runtime_is_expired=True)
```

#### Checking if a Runtime is Expiring

You can query if a runtime has a set expiry date by its identifier using the `runtime_is_expiring()` function.

```python
runtimes.runtime_is_expiring("nodejs")
>>> True
```

#### Checking if a Runtime has Expired

You can query if a runtime has expired by its identifier using the `runtime_is_expired()` function.

```python
runtimes.runtime_is_expired("nodejs")
>>> True
```

## The LambdaRuntime Data Class

The iterables and functions in the library mostly return instances of the `LambdaRuntime` class. This data class has fields that reflect the data on the AWS documentation website.

This data class is made with Pydantic and so type hints should work in your IDE of choice.

Each instance will have at least the following properties:

```python
name: str
identifier: str
sdk: Optional[str]
os: str
arch: Optional[str]
deprecation_phase_1: Optional[datetime] = None
deprecation_phase_2: Optional[datetime] = None
runtime_is_expiring: bool
runtime_is_expired: bool
```