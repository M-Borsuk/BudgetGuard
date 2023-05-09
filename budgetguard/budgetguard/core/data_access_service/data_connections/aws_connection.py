import boto3
from botocore.exceptions import ClientError
from base_connection import BaseConnection


class AWSConnection(BaseConnection):
    def get_aws_secret(self, secret_name: str, region_name: str = "us-east-1"):
        """
        Method to retrieve a secret from AWS Secrets Manager.

        :param secret_name: The name of the secret to retrieve.

        :return: The secret value.
        """
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager", region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e

        # Decrypts secret using the associated KMS key.
        secret = get_secret_value_response["SecretString"]
        return secret
