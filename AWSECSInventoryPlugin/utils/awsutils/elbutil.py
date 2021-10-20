from awsretry import AWSRetry

from base.aws_base_processor import AWSBaseProcessor


class ELB(AWSBaseProcessor):
    def __init__(self):
        super(ELB, self).__init__('elbv2')
        self.elb_client = super().get_service_client()
        pass

    @AWSRetry.backoff()
    def get_albtg_details(self, albtg_arn):
        return self.elb_client.describe_target_groups(TargetGroupArns=[albtg_arn])

    @AWSRetry.backoff()
    def get_listner_details(self, alb_arn):
        return self.elb_client.describe_listeners(LoadBalancerArn=alb_arn)

    @AWSRetry.backoff()
    def get_alb_rules(self, listner_arn):
        return self.elb_client.describe_rules(ListenerArn=listner_arn)

    @AWSRetry.backoff()
    def delete_listner_rule(self, listner_arn):
        return self.elb_client.delete_rule(RuleArn=listner_arn)

    @AWSRetry.backoff()
    def delete_albtg(self, alb_rule_arn):
        return self.elb_client.delete_target_group(TargetGroupArn=alb_rule_arn)
