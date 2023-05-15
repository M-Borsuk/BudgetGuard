import os
from .utilities import functions
from loguru import logger
from . import get_nordigen_function


def lambda_handler(event, context):
    # Retrieve the source S3 bucket and key from the event
    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    source_key = event["Records"][0]["s3"]["object"]["key"]
    formatting_function = get_nordigen_function(event.get("data_type"))
    # Retrieve the destination bucket and key from environment variables
    destination_bucket = os.environ["DESTINATION_BUCKET"]
    destination_key = os.environ["DESTINATION_KEY"]
    data = functions.s3_read_json(source_bucket, source_key)
    data = formatting_function(data)
    functions.s3_write_json(data, destination_bucket, destination_key)
    logger.info(
        "Successfully copied data from {0} to {1}!".format(
            source_bucket, destination_bucket
        )
    )
