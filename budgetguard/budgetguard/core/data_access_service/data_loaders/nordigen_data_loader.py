from .data_loader import DataLoader
from ..data_connections import connect
from loguru import logger


class NordigenDataLoader(DataLoader):
    NAME = "nordigen"

    def __init__(self):
        """
        Constructor for NordigenDataLoader class.
        """
        self.nordigen_connection = connect(self.NAME)
        self.accounts = self.nordigen_connection.accounts

    def read(self):
        """
        Method for reading data from the Nordigen API.
        """
        logger.info("Reading data from Nordigen...")
        output = {}
        for account in self.accounts:
            meta_data = account.get_metadata()
            details = account.get_details()
            balances = account.get_balances()
            transactions = account.get_transactions()
            output[meta_data["id"]] = {
                "details": details,
                "balances": balances,
                "transactions": transactions,
                "metadata": meta_data,
            }
        logger.info("Finished reading {0} accounts data!".format(len(output)))
        return output

    def write(self):
        """
        Method for writing data to the Nordigen API.
        """
        raise NotImplementedError(
            "Nordigen data loader doesn't support writing data."
        )
