import requests
from bs4 import BeautifulSoup
import logging
from dateutil import parser
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator

class LambdaRuntime(BaseModel):
    name: str
    identifier: str
    os: str
    deprecation_phase_1: Optional[datetime] = None
    deprecation_phase_2: Optional[datetime] = None
    runtime_is_expiring: bool
    runtime_is_expired: bool
    
    def __str__(self):
        return f"{self.name} ({self.identifier}) - Deprecation Phase 1: {self.deprecation_phase_1}, Deprecation Phase 2: {self.deprecation_phase_2}"

class LambdaRuntimes():

    NOT_SCHEDULED = "Not scheduled"

    # Logger configuration
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    # URL for fetching Lambda runtimes
    lambda_runtime_docs_url = "https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html"

    # Requests SSL validation config
    validate_ssl = True

    # Internal storage
    expired_runtimes_title = "Deprecated runtimes"
    current_runtimes_title = "Supported runtimes"
    runtimes: List[LambdaRuntime] = []

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
            data.append([cell.text.strip() for cell in columns])

        for row in data:
            if len(row) == 0:
                continue

            processed_data.append(LambdaRuntime(
                name=row[0], 
                identifier=row[1],
                os=row[2],
                deprecation_phase_1=parser.parse(row[3]) if row[3] not in [self.NOT_SCHEDULED, "N/A"] else None,
                deprecation_phase_2=parser.parse(row[4]) if row[4] not in [self.NOT_SCHEDULED, "N/A"] else None,
                runtime_is_expiring=True if row[3] != self.NOT_SCHEDULED else False,
                runtime_is_expired=False))

        self.logger.debug(processed_data)
        
        return processed_data
    
    def __process_expired_runtimes(self, table):
        self.logger.info("Processing Expired Runtimes Table")
        data = []
        processed_data = []
        
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            data.append([cell.text.strip() for cell in columns])

        for row in data:
            if len(row) == 0:
                continue

            processed_data.append(LambdaRuntime(
                name=row[0], 
                identifier=row[1],
                os=row[2],
                deprecation_phase_1=parser.parse(row[3]) if row[3] not in [self.NOT_SCHEDULED, "N/A"] else None,
                deprecation_phase_2=parser.parse(row[4]) if row[4] not in [self.NOT_SCHEDULED, "N/A"] else None,
                runtime_is_expiring=True,
                runtime_is_expired=True))

        self.logger.debug(processed_data)
        
        return processed_data

    def __populate_lambda_runtime_lists(self):
        self.runtimes.clear()
        lambda_runtimes_response = requests.get(self.lambda_runtime_docs_url, verify=self.validate_ssl)
        
        if not lambda_runtimes_response.ok:
            self.logger.error("Failed to fetch Lambda Runtimes from AWS Website.")
            self.logger.error(lambda_runtimes_response.text)
            lambda_runtimes_response.raise_for_status()

        lambda_runtimes_webpage_text = lambda_runtimes_response.text

        soup = BeautifulSoup(lambda_runtimes_webpage_text, 'html.parser')

        current_runtime_table = soup.find('h2', text=self.current_runtimes_title).find_next('table')
        self.runtimes.extend(self.__process_current_runtimes(current_runtime_table))
        expired_runtime_table = soup.find('h2', text=self.expired_runtimes_title).find_next('table')
        self.runtimes.extend(self.__process_expired_runtimes(expired_runtime_table))

    def __iter__(self):
        return iter(self.runtimes)

    def get_runtime(self, runtime_key) -> LambdaRuntime:
        """
        Gets a single runtime from the list by the runtime key.

        get_runtime("nodejs") -> LambdaRuntime
        """
        for runtime in self.runtimes:
            if runtime.identifier == runtime_key:
                return runtime
            
        return None
    
    def runtime_is_expiring(self, runtime_key) -> bool:
        """
        Gets a boolean for whether the runtime has a defined deprecation date.

        runtime_is_expiring("nodejs") -> True
        """
        for runtime in self.runtimes:
            if runtime.identifier == runtime_key:
                return runtime.runtime_is_expiring
        
        return None
    
    def runtime_is_expired(self, runtime_key):
        """
        Gets a boolean for whether the runtime has passed its deprecation date.

        runtime_is_expired("nodejs") -> True
        """
        for runtime in self.runtimes:
            if runtime.identifier == runtime_key:
                return runtime.runtime_is_expired
        
        return None
