import sys
import os

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, ".."))

from loguru import logger  # noqa: E402
from pyspark.sql import DataFrame as SparkDataFrame  # noqa: E402
from .bronze_to_silver_pipeline import BronzeToSilverPipeline  # noqa: E402


class BronzeToSilverBalancesPipeline(BronzeToSilverPipeline):
    INPUT_DATA_LOADER = "spark_s3"
    OUTPUT_DATA_LOADER = "spark_s3"
    INPUT_LAYER = "bronze"
    OUTPUT_LAYER = "silver"
    INPUT_KEY = "balances"
    OUTPUT_KEY = "balances"

    def transform(self, source_df: SparkDataFrame) -> SparkDataFrame:
        """
        Transforms the data.

        :param source_df: The data to transform.
        :return: The transformed data.
        """
        logger.info("Transforming data.")
        transformed_df = source_df
        return transformed_df
