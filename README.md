# Lambda Runtimes

Python library for getting a list of all Lambda runtimes from AWS's documentation page, and interacting with it.

## Usage

Install the requirements with `pip3 install -r requirements.txt`

### Basic Usage

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