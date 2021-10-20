import boto3
import botocore

from .base_processor import BaseProcessor


class AWSBaseProcessor(BaseProcessor):
    service_client = None

    def __init__(self, aws_service_name):
        super().__init__()
        self.service = aws_service_name

    def get_service_client(self):
        """
        Create boto3 client using AWS credentials
        :return:client
        """
        # Do not create service client if already created
        if self.service_client:
            return self.service_client
        else:
            self.service_client = self.__create_session()
        return self.service_client

    def __create_session(self):
        """
        Create boto3 client using default credentials
        :return:
        """
        client_config = botocore.config.Config(
            max_pool_connections=100,
        )
        session = boto3.session.Session()
        return session.client(self.service, config=client_config)
