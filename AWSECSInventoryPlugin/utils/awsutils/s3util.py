from awsretry import AWSRetry

from base.aws_base_processor import AWSBaseProcessor


class S3(AWSBaseProcessor):
    def __init__(self):
        super(S3, self).__init__('s3')
        self.s3_client = super().get_service_client()
        pass

    def get_regional_s3_client(self, region):
        super(S3, self).__init__('s3')
        return self.get_service_client_with_region(region)

    @AWSRetry.backoff()
    def upload_file_to_s3(self, bucket_name, object_key, data):
        return self.s3_client.put_object(ACL='bucket-owner-full-control', Bucket=bucket_name, Key=object_key, Body=data, ContentType='application/json',
                                         ServerSideEncryption='AES256')

    @AWSRetry.backoff()
    def get_object(self, bucket_name, object_key):
        return self.s3_client.get_object(Bucket=bucket_name, Key=object_key)

    @AWSRetry.backoff()
    def head_object(self, bucket_name, object_key):
        return self.s3_client.head_object(Bucket=bucket_name, Key=object_key)

    @AWSRetry.backoff()
    def generate_presigned_url(self, regional_s3_client, s3_bucket_name, s3_key):
        parameters = {'Bucket': s3_bucket_name, 'Key': s3_key}
        return regional_s3_client.generate_presigned_url(ClientMethod='get_object', Params=parameters)

    @AWSRetry.backoff()
    def copy_object(self, source_key, bucket_name, destination_key):
        return self.s3_client.copy_object(ACL='bucket-owner-full-control', CopySource=source_key, Bucket=bucket_name, Key=destination_key)

    @AWSRetry.backoff()
    def list_objects(self, bucket, nginx_env_prefix, key, service_short_name):
        prefix = "{}{}-{}".format(key, nginx_env_prefix, service_short_name)
        return self.s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)

    @AWSRetry.backoff()
    def copy_s3_objects(self, environment, nginx_rule):
        dest_object_key = "{}/{}".format(environment.value["destination_key"], nginx_rule)
        copy_source = {'Bucket': environment.value["bucket"], 'Key': nginx_rule}
        return self.s3_client.copy_object(Bucket=environment.value["bucket"], Key=dest_object_key, CopySource=copy_source)

    @AWSRetry.backoff()
    def delete_s3_objects(self, environment, nginx_rules):
        formatted_nginx_rules = list()
        for nginx_rule in nginx_rules:
            formatted_nginx_rules.append({"Key": nginx_rule})
        objects = {"Objects": formatted_nginx_rules}
        return self.s3_client.delete_objects(Bucket=environment.value["bucket"], Delete=objects)
