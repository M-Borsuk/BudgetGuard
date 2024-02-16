from .data_loader import DataLoader
from ..data_connections import connect
from loguru import logger
from typing import Dict
import json


class S3DataLoader(DataLoader):
    NAME = "s3"

    def __init__(self):
        """
        Constructor for S3DataLoader class.
        """
        self.s3_connection = connect(self.NAME)

    def _build_s3_prefix(
        self, datalake_config: Dict[str, str], partition_config: Dict[str, str]
    ):
        """
        Method for building the S3 prefix.

        :param datalake_config: The configuration of the datalake to read from.
        :param partition_id: The partition of the datalake to read from.
        """
        return "{0}/{1}".format(
            datalake_config["datalake_key"],
            self.build_partition_path(partition_config),
        )

    def get_all_bucket_objects(
        self,
        s3_client,
        datalake_config: Dict[str, str],
        partition_config: Dict[str, str],
    ):
        """
        Method for getting all the objects in the S3 bucket.

        :param s3_client: The S3 client.
        :param datalake_config: The configuration of the datalake to read from.
        """
        prefix = self._build_s3_prefix(datalake_config, partition_config)
        response = s3_client.list_objects_v2(
            Bucket=datalake_config["datalake_bucket"],
            Prefix=prefix,
        )
        return response["Contents"]

    def _build_s3_file_key(self, key: str, file_extension: str):
        """
        Method for building the S3 file key.

        :param key: The key of the datalake to read from.
        :param file_extension: The file extension of the file to read.
        """
        return "{0}.{1}".format(key, file_extension)

    def read(
        self, datalake_config: Dict[str, str], partition_config: Dict[str, str]
    ):
        """
        Method for reading data from the S3 bucket.

        :param datalake_layer: The layer of the datalake to read from.
        :param datalake_key: The key of the datalake to read from.
        """
        logger.info("Reading data from S3...")
        s3_client = self.s3_connection.s3_client
        contents = self.get_all_bucket_objects(
            s3_client, datalake_config, partition_config
        )
        output = []
        for file in contents:
            key = file["Key"]
            response = s3_client.get_object(
                Bucket=datalake_config["datalake_bucket"],
                Key=key,
            )
            json_data = response["Body"].read().decode("utf-8")
            parsed_data = json.loads(json_data)
            output.append((key, parsed_data))
        logger.info("Finished reading data from S3!")
        return output

    def write(
        self,
        file_content,
        datalake_config: Dict[str, str],
        partition_config: Dict[str, str],
    ):
        """
        Method for writing data to the S3 bucket.

        :param datalake_layer: The layer of the datalake to write to.
        :param datalake_key: The key of the datalake to write to.
        """
        logger.info("Writing data to S3...")
        s3_client = self.s3_connection.s3_client
        prefix = self._build_s3_prefix(datalake_config, partition_config)
        key = self._build_s3_file_key(
            datalake_config["datalake_key"], datalake_config["file_extension"]
        )
        s3_client.put_object(
            Bucket=datalake_config["datalake_bucket"],
            Key="{0}/{1}".format(prefix, key),
            Body=file_content,
        )
