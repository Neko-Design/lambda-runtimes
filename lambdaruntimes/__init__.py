import requests
from bs4 import BeautifulSoup
import logging
from dateutil import parser

class LambdaRuntimes():

    # Logger configuration
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    # URL for fetching Lambda runtimes
    lambda_runtime_docs_url = "https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html"

    # Requests SSL validation config
    validate_ssl = True

    # Internal storage
    expired_runtimes_title = "Deprecated runtimes"
    current_runtimes_title = "Supported Runtimes"
    runtimes = []

    def __init__(self, validate_ssl = True, lambda_runtime_docs_url = None):
        self.validate_ssl = validate_ssl
        self.lambda_runtime_docs_url = lambda_runtime_docs_url if lambda_runtime_docs_url is not None else self.lambda_runtime_docs_url

        self.__populate_lambda_runtime_lists()

    def __process_current_runtimes(self, table):
        self.logger.info("Processing Current Runtimes Table")
        data = []
        processed_data = []
        
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            column_data = [cell.text.strip() for cell in columns]
            data.append([cell for cell in column_data])

        for row in data:
            if len(row) == 0:
                continue
            processed_data.append({
                "runtime_name": row[0],
                "runtime_key": row[1],
                "runtime_deprecation": parser.parse(row[5]) if row[5] else None,
                "runtime_expiry": None,
                "runtime_is_expiring": True if row[5] else False,
                "runtime_expired": False
            })

        self.logger.debug(processed_data)
        
        return processed_data
    
    def __process_expired_runtimes(self, table):
        self.logger.info("Processing Expired Runtimes Table")
        data = []
        processed_data = []
        
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            column_data = [cell.text.strip() for cell in columns]
            data.append([cell for cell in column_data])

        for row in data:
            if len(row) == 0:
                continue
            processed_data.append({
                "runtime_name": row[0],
                "runtime_key": row[1],
                "runtime_deprecation": parser.parse(row[3]) if row[3] else parser.parse(row[4]),
                "runtime_expiry": parser.parse(row[4]),
                "runtime_is_expiring": True,
                "runtime_expired": True
            })

        self.logger.debug(processed_data)
        
        return processed_data

    def __populate_lambda_runtime_lists(self):
        lambda_runtimes_response = requests.get(self.lambda_runtime_docs_url, verify=self.validate_ssl)
        
        if not lambda_runtimes_response.ok:
            self.logger.error("Failed to fetch Lambda Runtimes from AWS Website.")
            self.logger.error(lambda_runtimes_response.text)
            lambda_runtimes_response.raise_for_status()

        lambda_runtimes_webpage_text = lambda_runtimes_response.text

        soup = BeautifulSoup(lambda_runtimes_webpage_text, 'html.parser')

        tables = soup.find_all('table')

        for table in tables:
            table_title = table.css.select_one('.title').get_text()
            if table_title == self.current_runtimes_title:
                self.runtimes.extend(self.__process_current_runtimes(table))
            elif table_title == self.expired_runtimes_title:
                self.runtimes.extend(self.__process_expired_runtimes(table))
            else:
                self.logger.warn("Unknown Table: {}".format(table_title))

    def get_runtime(self, runtime_key) -> dict:
        """
        Gets a single runtime from the list by the runtime key.

        get_runtime("nodejs") -> dict
        """
        for runtime in self.runtimes:
            if runtime.get('runtime_key') == runtime_key:
                return runtime
            
        return None
    
    def runtime_is_expiring(self, runtime_key) -> bool:
        """
        Gets a boolean for whether the runtime has a defined deprecation date.

        runtime_is_expiring("nodejs") -> True
        """
        for runtime in self.runtimes:
            if runtime.get('runtime_key') == runtime_key:
                return runtime.get('runtime_is_expiring')
        
        return None
    
    def runtime_is_expired(self, runtime_key):
        """
        Gets a boolean for whether the runtime has passed its deprecation date.

        runtime_is_expired("nodejs") -> True
        """
        for runtime in self.runtimes:
            if runtime.get('runtime_key') == runtime_key:
                return runtime.get('runtime_expired')
        
        return None