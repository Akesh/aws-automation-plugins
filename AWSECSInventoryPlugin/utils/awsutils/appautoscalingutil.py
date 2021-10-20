from awsretry import AWSRetry

from base.aws_base_processor import AWSBaseProcessor


class ApplicationAutoscaling(AWSBaseProcessor):
    def __init__(self):
        super(ApplicationAutoscaling, self).__init__('application-autoscaling')
        self.app_autoscaling_client = super().get_service_client()
        pass

    @AWSRetry.backoff()
    def get_scalable_target_details(self, cluster_name, service_name):
        resource_ids = ["service/{}/{}".format(cluster_name, service_name)]
        return self.app_autoscaling_client.describe_scalable_targets(ServiceNamespace="ecs", ScalableDimension="ecs:service:DesiredCount", ResourceIds=resource_ids)

    @AWSRetry.backoff()
    def register_scalable_target_details(self, cluster_name, service_name, min_capacity, max_capacity):
        resource_id = "service/{}/{}".format(cluster_name, service_name)
        return self.app_autoscaling_client.register_scalable_target(ServiceNamespace="ecs", ScalableDimension="ecs:service:DesiredCount", ResourceId=resource_id,
                                                                    MinCapacity=min_capacity,
                                                                    MaxCapacity=max_capacity)
