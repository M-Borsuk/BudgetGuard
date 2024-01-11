import sys
import os

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, ".."))

from loguru import logger  # noqa: E402
from pyspark.sql import DataFrame as SparkDataFrame  # noqa: E402
from .bronze_to_silver_pipeline import BronzeToSilverPipeline  # noqa: E402
import pyspark.sql.functions as F  # noqa: E402


class BronzeToSilverTransactionsPipeline(BronzeToSilverPipeline):
    INPUT_DATA_LOADER = "spark_s3"
    OUTPUT_DATA_LOADER = "spark_s3"
    INPUT_LAYER = "bronze"
    OUTPUT_LAYER = "silver"
    INPUT_KEY = "transactions"
    OUTPUT_KEY = "transactions"

    def transform(self, source_df: SparkDataFrame) -> SparkDataFrame:
        """
        Transforms the data.

        :param source_df: The data to transform.
        :return: The transformed data.
        """
        logger.info("Transforming data.")
        transformed_df = source_df.withColumn(
            "creditor_account_iban",
            F.col("creditor_account.iban").cast("string"),
        )
        transformed_df = transformed_df.withColumn(
            "remittance_information_unstructured",
            F.explode("remittance_information_unstructured_array"),
        )
        return transformed_df
