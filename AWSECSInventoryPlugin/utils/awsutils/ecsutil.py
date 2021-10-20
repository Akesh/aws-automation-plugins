from awsretry import AWSRetry

from base.aws_base_processor import AWSBaseProcessor


class ECS(AWSBaseProcessor):
    def __init__(self):
        super(ECS, self).__init__('ecs')
        self.ecs_client = super().get_service_client()
        pass

    @AWSRetry.backoff()
    def get_clusters_list(self):
        return self.ecs_client.list_clusters()

    @AWSRetry.backoff()
    def get_service_list(self, cluster_arn):
        ecs_services_list = list()
        list_services_response = self.ecs_client.list_services(cluster=cluster_arn)
        while True:
            ecs_services_list.extend(list_services_response['serviceArns'])
            if "nextToken" in list_services_response:
                list_services_response = self.ecs_client.list_services(cluster=cluster_arn, nextToken=list_services_response['nextToken'])
                continue
            else:
                break
        return ecs_services_list

    @AWSRetry.backoff()
    def get_service_details(self, cluster_arn, service_name):
        return self.ecs_client.describe_services(cluster=cluster_arn, services=[service_name])

    @AWSRetry.backoff()
    def get_task_definition_details(self, task_defintion):
        return self.ecs_client.describe_task_definition(taskDefinition=task_defintion)

    @AWSRetry.backoff()
    def delete_ecs_service(self, cluster_arn, service_name):
        return self.ecs_client.delete_service(cluster=cluster_arn, service=service_name, force=True)

    @AWSRetry.backoff()
    def list_task_definitions(self, task_definition_family):
        task_definitions_list_response = self.ecs_client.list_task_definitions(familyPrefix=task_definition_family, status="ACTIVE")
        task_definition_arns = list()
        while True:
            task_definition_arns.extend(task_definitions_list_response['taskDefinitionArns'])
            if "nextToken" in task_definition_arns:
                task_definitions_list_response = self.ecs_client.list_task_definitions(amilyPrefix=task_definition_family, status="ACTIVE",
                                                                                       nextToken=task_definitions_list_response['nextToken'])
                continue
            else:
                break
        return task_definition_arns
        pass

    @AWSRetry.backoff()
    def deregister_task_definitions(self, task_definition_arn):
        return self.ecs_client.deregister_task_definition(taskDefinition=task_definition_arn)

    @AWSRetry.backoff()
    def update_ecs_service_tasks(self, cluster_name, service_name, desired_task_count):
        return self.ecs_client.update_service(cluster=cluster_name, service=service_name, desiredCount=desired_task_count)

    @AWSRetry.backoff()
    def list_ecs_container_instances(self, ecs_cluster_arn):
        """
        This will return ARNs of all container instances running under an ECS cluster
        :param ecs_cluster_arn:
        :return:
        """
        return self.ecs_client.list_container_instances(cluster=ecs_cluster_arn)

    @AWSRetry.backoff()
    def describe_ecs_container_instances(self, ecs_cluster_arn, container_instance_arns):
        """
        This will return all details of a container instance in an ECS cluster. We will need instance_id from this response
        :param ecs_cluster_arn:
        :param container_instance_arns:
        :return:
        """
        return self.ecs_client.describe_container_instances(cluster=ecs_cluster_arn, containerInstances=container_instance_arns)

    @AWSRetry.backoff()
    def get_ecs_cluster_name_by_arn(self, ecs_cluster_arn):
        """
        Retrieve cluster name from arn. arn:aws:ecs:REGION:ACCOUNT_ID:cluster/CLUSTER_NAME
        :param ecs_cluster_arn:
        :return:
        """
        return ecs_cluster_arn.split("/")[1]

    @AWSRetry.backoff()
    def get_service_details(self, cluster_arn):
        service_details = self.ecs_client.list_services(cluster=cluster_arn, maxResults=100)
        return service_details

    @AWSRetry.backoff()
    def get_paginated_service_details(self, cluster_arn, nextToken):
        service_details = self.ecs_client.list_services(cluster=cluster_arn, nextToken=nextToken, maxResults=100)
        return service_details

    @AWSRetry.backoff()
    # def get_ecs_service_name_in_arn(service_arn):
    #     """
    #     Retrieve service name out of service arn. ARN format is arn:aws:ecs:REGION:ACCOUNT_ID:service/SERVICE_NAME
    #     :param service_arn:
    #     :return: service_name
    #     """
    #     return str(service_arn).split("/")[1]

    @AWSRetry.backoff()
    def get_ecs_service_name_in_arn(self, service_arn):
        """
        Retrieve service name out of service arn.
        ARN format is arn:aws:ecs:REGION:ACCOUNT_ID:service/SERVICE_NAME or arn:aws:ecs:REGION:ACCOUNT_ID:service/CLUSTER_NAME/SERVICE_NAME
        :param service_arn:
        :return: service_name
        """
        split_arn = str(service_arn).split("/")
        if len(split_arn) > 2:
            return split_arn[2]
        return split_arn[1]

    @AWSRetry.backoff()
    def describe_ecs_services(self, ecs_cluster_arn, ecs_services_arn):
        """
        Describe ECS services running in an ECS cluster
        :param ecs_cluster_arn:
        :param ecs_services_arn:
        :return:
        """
        return self.ecs_client.describe_services(cluster=ecs_cluster_arn, services=ecs_services_arn)

    # #################### All ECS TASKS FUNCTIONS GO HERE ########################
    @AWSRetry.backoff()
    def get_ecs_tasks_list(self, ecs_cluster_arn, service_details):
        """
        Get list of all ECS tasks running under mentioned cluster and services
        :param ecs_cluster_arn:
        :param service_details:
        :return:
        """
        return self.ecs_client.list_tasks(cluster=ecs_cluster_arn, serviceName=service_details)

    @AWSRetry.backoff()
    def describe_ecs_tasks(self, ecs_cluster_arn, tasks_arn_list):
        """
        Describe ECS task running under an ECS cluster
        :param ecs_cluster_arn:
        :param tasks_arn_list:
        :return:
        """
        return self.ecs_client.describe_tasks(cluster=ecs_cluster_arn, tasks=tasks_arn_list)

    @AWSRetry.backoff()
    def list_ecs_clusters(self):
        ecs_clusters_list_response = self.ecs_client.list_clusters()
        ecs_cluster_arns = list()
        while True:
            ecs_cluster_arns.extend(ecs_clusters_list_response['clusterArns'])
            if "nextToken" in ecs_clusters_list_response:
                ecs_clusters_list_response = self.ecs_client.list_clusters(nextToken=ecs_clusters_list_response['nextToken'])
                continue
            else:
                break
        return ecs_cluster_arns
