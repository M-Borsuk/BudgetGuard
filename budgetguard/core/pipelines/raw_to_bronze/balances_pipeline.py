import sys
import os
from loguru import logger
from typing import List, Dict

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, ".."))

from .raw_to_bronze_pipeline import RawToBronzePipeline  # noqa: E402


class RawToBronzeBalancesPipeline(RawToBronzePipeline):
    INPUT_KEY = "balances"
    OUTPUT_KEY = "balances"

    def transform(self, source_data: List[Dict[str, str]]):
        """
        Transforms the data.

        :param source_data: The data to transform.
        :return: The transformed data.
        """
        logger.info("Transforming data.")
        return [
            (acc_id, self.format_balances(data))
            for acc_id, data_object in source_data
            for key, data in data_object
        ]

    def format_balances(self, balances):
        """
        Formats the balances.

        :param balances: The balances to format.
        :return: The formatted balances.
        """
        balances_flattened = balances.get("balances", {})
        balances_flattened = [
            {
                "balanceAmount": balance.get("balanceAmount", {}).get(
                    "amount", ""
                ),
                "balanceCurrency": balance.get("balanceAmount", {}).get(
                    "currency", ""
                ),
                "balanceType": balance.get("balanceType", ""),
            }
            for balance in balances_flattened
        ]
        balances_flattened = [
            {self.camel_to_snake(key): value for key, value in balance.items()}
            for balance in balances_flattened
        ]
        return balances_flattened
