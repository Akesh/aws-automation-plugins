from awsretry import AWSRetry

from base.aws_base_processor import AWSBaseProcessor


class EC2(AWSBaseProcessor):
    def __init__(self):
        super(EC2, self).__init__('ec2')
        self.ec2_client = super().get_service_client()
        pass
