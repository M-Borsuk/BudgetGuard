from .connection import Connection
from .aws_connection import AWSConnection
from forex_python.converter import CurrencyRates, RatesNotAvailableError
import requests
import json
from loguru import logger


class ExchangeRatesAPIConnection(Connection):
    class CustomCurrencyRates(CurrencyRates):
        def __init__(
            self,
            backup_access_key: str,
            force_decimal=False,
            backup_source="http://api.exchangerate.host/",
        ):
            super().__init__(force_decimal)
            self.backup_source = backup_source
            self.backup_access_key = backup_access_key

        def get_rates_backup(self, base_cur, date_obj=None):
            date_str = self._get_date_string(date_obj)
            if date_str == "latest":
                postfix = "live"
            else:
                postfix = "historical"
            payload = {
                "source": base_cur,
                "date": date_str,
                "access_key": self.backup_access_key,
            }
            source_url = self.backup_source + postfix
            response = requests.get(source_url, params=payload)
            data = response.json()
            exchange_rates = data["quotes"]
            return {
                key.replace(base_cur, ""): value
                for key, value in exchange_rates.items()
            }

        def get_rates_with_backup(self, base_cur, date_obj=None):
            try:
                logger.info(f"Getting exchange rates for {base_cur}...")
                return self.get_rates(base_cur, date_obj)
            except (
                RatesNotAvailableError,
                requests.exceptions.ConnectionError,
            ):
                logger.warning(
                    f"Exchange rates for {base_cur} not available. Using backup source..."  # noqa
                )
                return self.get_rates_backup(base_cur, None)

    def __init__(self) -> None:
        super().__init__()
        self.aws_connection: AWSConnection = AWSConnection()
        self.exchange_rates_secret = json.loads(
            self.aws_connection.get_aws_secret(
                "budgetguard_exchange_rates_api_backup"
            )
        )
        self.connection: self.CustomCurrencyRates = self.connect()

    def connect(self):
        return self.CustomCurrencyRates(
            backup_access_key=self.exchange_rates_secret["access_key"],
            backup_source=self.exchange_rates_secret["source_url"],
        )
