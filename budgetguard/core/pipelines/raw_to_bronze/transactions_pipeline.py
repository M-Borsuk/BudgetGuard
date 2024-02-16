import sys
import os
from loguru import logger
from typing import List, Dict

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, ".."))

from .raw_to_bronze_pipeline import RawToBronzePipeline  # noqa: E402


class RawToBronzeTransactionsPipeline(RawToBronzePipeline):
    INPUT_KEY = "transactions"
    OUTPUT_KEY = "transactions"

    def transform(self, source_data: List[Dict[str, str]]):
        """
        Transforms the data.

        :param source_data: The data to transform.
        :return: The transformed data.
        """
        logger.info("Transforming data.")
        return [
            (acc_id, self.format_transactions(data))
            for acc_id, data_object in source_data
            for key, data in data_object
        ]

    def format_transactions(self, transactions):
        """
        Formats the transactions.

        :param transactions: The transactions to format.
        :return: The formatted transactions.
        """
        transactions_flatten = []
        logger.info("Flattening transactions...")
        for transaction_status, transactions_info in transactions[
            "transactions"
        ].items():
            logger.info(
                "Flattening transactions for status {0}...".format(
                    transaction_status
                )
            )  # noqa
            logger.info(
                "Number of transactions with status {0}: {1}".format(
                    transaction_status, len(transactions_info)
                )
            )
            for transaction in transactions_info:
                transaction["transactionStatus"] = transaction_status
                transaction["transactionCurrency"] = transaction[
                    "transactionAmount"
                ]["currency"]
                transaction["transactionAmount"] = transaction[
                    "transactionAmount"
                ]["amount"]
                if transaction.get("debtorAccount"):
                    transaction["debtorAccountIban"] = transaction[
                        "debtorAccount"
                    ]["iban"]
                    del transaction["debtorAccount"]
                else:
                    transaction["creditorAccountIban"] = transaction[
                        "creditorAccount"
                    ]["iban"]
                    del transaction["creditorAccount"]
                transaction["balanceAfterTransactionAmount"] = transaction[
                    "balanceAfterTransaction"
                ]["balanceAmount"]["amount"]
                transaction["balanceAfterTransactionCurrency"] = transaction[
                    "balanceAfterTransaction"
                ]["balanceAmount"]["currency"]
                del transaction["remittanceInformationUnstructured"]
                del transaction["balanceAfterTransaction"]
                transactions_flatten.append(
                    {self.camel_to_snake(k): v for k, v in transaction.items()}
                )
        logger.info("Finished flattening transactions!")
        return transactions_flatten
