import sys
import os

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, ".."))

from ..pipeline import Pipeline  # noqa: E402
from ...datalake import Datalake  # noqa: E402
from ...data_access_service.data_loaders import (  # noqa: E402
    create_data_loader,
)
from loguru import logger  # noqa: E402
from pyspark.sql import DataFrame as SparkDataFrame  # noqa: E402
from abc import abstractmethod  # noqa: E402


class BronzeToSilverPipeline(Pipeline):
    INPUT_DATA_LOADER = "spark_s3"
    OUTPUT_DATA_LOADER = "spark_s3"
    INPUT_LAYER = "bronze"
    OUTPUT_LAYER = "silver"

    def __init__(self, partition_id: str) -> None:
        self.datalake = Datalake()
        self.partition_id = partition_id
        self.input_loader = create_data_loader(self.INPUT_DATA_LOADER)
        self.output_loader = create_data_loader(self.OUTPUT_DATA_LOADER)

    def read_sources(self) -> SparkDataFrame:
        """
        Reads the data from the data sources.

        :return: The data from the data sources.
        """
        logger.info("Reading data from datalake.")
        source_df = self.input_loader.read(
            self.datalake[self.INPUT_LAYER][self.INPUT_KEY],
            {
                "partition_id": self.partition_id,
            },
        )
        return source_df

    def write_sources(self, transformed_df: SparkDataFrame):
        """
        Writes the data to the data sources.

        :param transformed_df: The transformed data.
        """
        logger.info("Writing data to datalake.")
        self.output_loader.write(
            transformed_df,
            self.datalake[self.OUTPUT_LAYER][self.OUTPUT_KEY],
            {"partition_id": self.partition_id},
        )

    @abstractmethod
    def transform(self, source_df: SparkDataFrame) -> SparkDataFrame:
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
        source_df = self.read_sources()
        transformed_df = self.transform(source_df)
        self.write_sources(transformed_df)