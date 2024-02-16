import sys
import os
from loguru import logger
from typing import List, Dict

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, ".."))

from .raw_to_bronze_pipeline import RawToBronzePipeline  # noqa: E402


class RawToBronzeMetadataPipeline(RawToBronzePipeline):
    INPUT_KEY = "metadata"
    OUTPUT_KEY = "metadata"

    def transform(self, source_data: List[Dict[str, str]]):
        """
        Transforms the data.

        :param source_data: The data to transform.
        :return: The transformed data.
        """
        logger.info("Transforming data.")
        return [
            (acc_id, self.format_metadata(data))
            for acc_id, data_object in source_data
            for key, data in data_object
        ]

    def format_metadata(self, metadata):
        """
        Formats the metadata.

        :param metadata: The metadata to format.
        :return: The formatted metadata.
        """
        return metadata
