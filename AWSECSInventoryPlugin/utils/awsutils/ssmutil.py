from awsretry import AWSRetry

from base.aws_base_processor import AWSBaseProcessor


class SSM(AWSBaseProcessor):
    def __init__(self):
        super(SSM, self).__init__('ssm')
        self.ssm_client = super().get_service_client()
        pass

    @AWSRetry.backoff()
    def execute_automation_document(self, ssm_document_name, ssm_document_version, reboot_required, instance_id, ami_name, delete_on_date):
        parameters = {"InstanceId": [instance_id], "NoReboot": [reboot_required], "AMINameValue": [ami_name], "DeleteOnValue": [delete_on_date]}
        return self.ssm_client.start_automation_execution(DocumentName=ssm_document_name, DocumentVersion=ssm_document_version, Parameters=parameters)

    @AWSRetry.backoff()
    def describe_automation_execution_with_id(self, automation_execution_id):
        filters = [{'Key': 'ExecutionId', 'Values': [automation_execution_id]}]
        return self.ssm_client.describe_automation_executions(Filters=filters)

    @AWSRetry.backoff()
    def get_automation_execution_with_id(self, automation_execution_id):
        return self.ssm_client.get_automation_execution(AutomationExecutionId=automation_execution_id)

    @AWSRetry.backoff()
    def send_command_for_scan(self, patch_baseline_document, patch_baseline_document_version, patch_baseline_mode, patch_baseline_reboot, instance_id, comments,
                              patch_baseline_timeout, ssm_command_output_bucket, ssm_command_output_s3_key_prefix):
        parameters = {'Operation': [patch_baseline_mode], 'RebootOption': [patch_baseline_reboot]}
        return self.ssm_client.send_command(InstanceIds=[instance_id], DocumentName=patch_baseline_document, DocumentVersion=patch_baseline_document_version,
                                            TimeoutSeconds=patch_baseline_timeout, Comment=comments, Parameters=parameters, OutputS3BucketName=ssm_command_output_bucket,
                                            OutputS3KeyPrefix=ssm_command_output_s3_key_prefix)

    @AWSRetry.backoff()
    def send_shell_command(self, instance_id, run_command_document, run_command_document_version, run_command_output_bucket, run_command_output_s3_key_prefix, commands, comments,
                           run_command_timeout):
        parameters = {'commands': commands}
        return self.ssm_client.send_command(InstanceIds=[instance_id], DocumentName=run_command_document, DocumentVersion=run_command_document_version, Parameters=parameters,
                                            Comment=comments,
                                            OutputS3BucketName=run_command_output_bucket, OutputS3KeyPrefix=run_command_output_s3_key_prefix, TimeoutSeconds=run_command_timeout)

    @AWSRetry.backoff()
    def get_command_invocation(self, command_id, instance_id):
        return self.ssm_client.list_command_invocations(CommandId=command_id, Details=True)

    @AWSRetry.backoff()
    def describe_instance_patches(self, instance_id, filter_key, filter_value):
        filters = [{'Key': filter_key, 'Values': filter_value}]
        return self.ssm_client.describe_instance_patches(InstanceId=instance_id, Filters=filters)

    @AWSRetry.backoff()
    def send_command_for_install(self, patch_baseline_document, patch_baseline_document_version, patch_baseline_mode, patch_baseline_reboot, instance_id, comments,
                                 pb_override_patch_data_file_url, patch_baseline_timeout, ssm_command_output_bucket, ssm_command_output_s3_key_prefix):
        parameters = {'Operation': [patch_baseline_mode], 'RebootOption': [patch_baseline_reboot], 'InstallOverrideList': [pb_override_patch_data_file_url]}
        return self.ssm_client.send_command(InstanceIds=[instance_id], DocumentName=patch_baseline_document, DocumentVersion=patch_baseline_document_version,
                                            TimeoutSeconds=patch_baseline_timeout, Comment=comments, Parameters=parameters, OutputS3BucketName=ssm_command_output_bucket,
                                            OutputS3KeyPrefix=ssm_command_output_s3_key_prefix)

    @AWSRetry.backoff()
    def describe_instance_patch_states(self, instance_id):
        return self.ssm_client.describe_instance_patch_states(InstanceIds=[instance_id])

    @AWSRetry.backoff()
    def describe_instance_information(self, instance_id):
        filters = [{'Key': "InstanceIds", 'Values': [instance_id]}]
        return self.ssm_client.describe_instance_information(Filters=filters)