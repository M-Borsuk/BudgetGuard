from conftest import SparkETLTestCase
from pyspark.sql.types import *


class TestDummy(SparkETLTestCase):
    def test_base(self):
        # 1. Prepare an input data frame that mimics our source data.
        input_schema = StructType(
            [
                StructField("StoreID", IntegerType(), True),
                StructField("Location", StringType(), True),
                StructField("Date", StringType(), True),
                StructField("ItemCount", IntegerType(), True),
            ]
        )
        input_data = [
            (1, "Bangalore", "2021-12-01", 5),
            (2, "Bangalore", "2021-12-01", 3),
            (5, "Amsterdam", "2021-12-02", 10),
            (6, "Amsterdam", "2021-12-01", 1),
            (8, "Warsaw", "2021-12-02", 15),
            (7, "Warsaw", "2021-12-01", 99),
        ]
        input_df = self.spark.createDataFrame(
            data=input_data, schema=input_schema
        )
        input_df.collect()
