import boto3
import json
from typing import Dict


def s3_read_json(source_bucket: str, source_key: str) -> Dict:
    """
    Method for reading a JSON file from S3.
    """

    # Create an S3 client
    s3 = boto3.client("s3")

    try:
        # Retrieve the JSON data from the source S3 object
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        json_data = response["Body"].read().decode("utf-8")

        # Parse the JSON data
        parsed_data = json.loads(json_data)

        # Convert the parsed data back to JSON format
        json_output = json.dumps(parsed_data)

        return json_output

    except Exception as e:
        print("Error: {}".format(str(e)))
        return {"statusCode": 500, "body": "Error: {}".format(str(e))}


def s3_write_json(json_data: str, target_bucket: str, target_key: str) -> Dict:
    """
    Method for writing a JSON file to S3.
    """

    # Create an S3 client
    s3 = boto3.client("s3")

    try:
        # Write the JSON string to the target S3 object
        response = s3.put_object(
            Bucket=target_bucket, Key=target_key, Body=json_data
        )

        return response

    except Exception as e:
        print("Error: {}".format(str(e)))
        return {"statusCode": 500, "body": "Error: {}".format(str(e))}
