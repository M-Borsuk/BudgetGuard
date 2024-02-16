import sys
import os
from loguru import logger
from abc import abstractmethod
import re
from typing import List, Dict
import json

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, ".."))

from ..pipeline import Pipeline  # noqa: E402
from ...datalake import Datalake  # noqa: E402
from ...data_access_service.data_loaders import (  # noqa: E402
    create_data_loader,
)


class RawToBronzePipeline(Pipeline):
    INPUT_DATA_LOADER = "s3"
    OUTPUT_DATA_LOADER = "s3"
    INPUT_LAYER = "ingest"
    OUTPUT_LAYER = "bronze"

    def __init__(self, partition_id: str) -> None:
        self.datalake = Datalake()
        self.partition_id = partition_id
        self.input_loader = create_data_loader(self.INPUT_DATA_LOADER)
        self.output_loader = create_data_loader(self.OUTPUT_DATA_LOADER)
        self.account_ids = self.__get_account_ids__()

    def read_sources(self) -> List[Dict[str, str]]:
        """
        Reads the data from the data sources.

        :return: The data from the data sources.
        """
        logger.info("Reading data from datalake.")
        return [
            (
                account_id,
                self.input_loader.read(
                    self.datalake[self.INPUT_LAYER][self.INPUT_KEY],
                    {
                        "partition_id": self.partition_id,
                        "account_id": account_id,
                    },
                ),
            )
            for account_id in self.account_ids
        ]

    def write_sources(self, transformed_data: List[Dict[str, str]]):
        """
        Writes the data to the data sources.

        :param transformed_df: The transformed data.
        """
        logger.info("Writing data to datalake.")
        datalake_config = self.datalake[self.OUTPUT_LAYER][self.OUTPUT_KEY]
        for account_id, data in transformed_data:
            print(account_id, data)
            partition_config = {
                "partition_id": self.partition_id,
                "account_id": account_id,
            }
            logger.info(
                f"Writing data to datalake for account_id: {account_id}"
            )
            self.output_loader.write(
                json.dumps(data), datalake_config, partition_config
            )

    @abstractmethod
    def transform(
        self, source_data: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """
        Transforms the data.

        :param source_df: The data to transform.
        :return: The transformed data.
        """
        raise NotImplementedError("Transform method not implemented!")

    def run(self):
        """
        Runs the pipeline.
        """
        logger.info("Running the bronze to silver pipeline...")
        source_data = self.read_sources()
        transformed_data = self.transform(source_data)
        self.write_sources(transformed_data)
        logger.info("Bronze to silver pipeline completed.")

    def __get_account_ids__(self) -> List[str]:
        """
        Gets the account ids from s3 bucket for the given partition
        by getting the paths of the files in the bucket.

        :return: The account ids.
        """
        s3_client = self.input_loader.s3_connection.s3_client
        contents = self.input_loader.get_all_bucket_objects(
            s3_client,
            self.datalake[self.INPUT_LAYER][self.INPUT_KEY],
            {"partition_id": self.partition_id},
        )
        return [
            re.search(r"account_id=(.*?)/", content["Key"]).group(1)
            for content in contents
        ]

    @staticmethod
    def camel_to_snake(s: str) -> str:
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
