from awsretry import AWSRetry

from base.aws_base_processor import AWSBaseProcessor


class ECR(AWSBaseProcessor):
    def __init__(self):
        super(ECR, self).__init__('ecr')
        self.ecr_client = super().get_service_client()
        pass

    @AWSRetry.backoff()
    def delete_ecr_repositiry(self, ecr_registry):
        return self.ecr_client.delete_repository(repositoryName=ecr_registry, force=True)
