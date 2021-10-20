from awsretry import AWSRetry

from base.aws_base_processor import AWSBaseProcessor


class R53(AWSBaseProcessor):
    def __init__(self):
        super(R53, self).__init__('route53')
        self.r53_client = super().get_service_client()
        pass

    @AWSRetry.backoff()
    def list_resource_records(self, hosted_zone_id, r53_record_name, ):
        return self.r53_client.list_resource_record_sets(HostedZoneId=hosted_zone_id, StartRecordName=r53_record_name)

    @AWSRetry.backoff()
    def delete_r53_record(self, hosted_zone_id, resource_record_set):
        resource_record_change = {"Comment": "Service Decommission Request", "Changes": [{"Action": "DELETE", "ResourceRecordSet": resource_record_set}]}
        # return self.r53_client.change_resource_record_sets(HostedZoneId=hosted_zone_id, ChangeBatch=resource_record_change)
        pass
