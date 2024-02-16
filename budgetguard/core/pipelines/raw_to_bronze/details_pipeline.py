import sys
import os
from loguru import logger
from typing import List, Dict

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, ".."))

from .raw_to_bronze_pipeline import RawToBronzePipeline  # noqa: E402


class RawToBronzeDetailsPipeline(RawToBronzePipeline):
    INPUT_KEY = "details"
    OUTPUT_KEY = "details"

    def transform(self, source_data: List[Dict[str, str]]):
        """
        Transforms the data.

        :param source_data: The data to transform.
        :return: The transformed data.
        """
        logger.info("Transforming data.")
        return [
            (acc_id, self.format_details(data))
            for acc_id, data_object in source_data
            for key, data in data_object
        ]

    def format_details(self, details):
        """
        Formats the details.

        :param details: The details to format.
        :return: The formatted details.
        """
        details_flattened = details.get("account", {})
        details_flattened = {
            self.camel_to_snake(k): v for k, v in details_flattened.items()
        }
        return details_flattened
