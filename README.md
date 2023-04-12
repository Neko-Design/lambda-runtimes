# Lambda Runtimes

Python library for getting a list of all Lambda runtimes from AWS's documentation page, and interacting with it.

## Usage

Install the requirements with `pip3 install -r requirements.txt`

### Basic Usage

Import the library at the top of your python file and create an instance of the `LambdaRuntimes` class. This fetches a list of the runtimes from the AWS docs page.

```python
import lambdaruntimes
runtimes = lambdaruntimes.LambdaRuntimes()
```

You can optionally specify another location for the source docs page if you have a cache or proxy.

```python
runtimes = lambdaruntimes.LambdaRuntimes(lambda_runtime_docs_url="http://localhost:8000/lambda-runtimes.html")
```

### Getting a Single Runtime

You can query for a runtime by its key using the `get_runtime()` function.

```python
runtimes.get_runtime("nodejs")
```