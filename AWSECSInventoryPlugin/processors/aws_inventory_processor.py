import logging
import threading

from base.base_processor import BaseProcessor
from utils import helper
from utils.awsutils.ecsutil import ECS


class AWSInventoryProcessor(BaseProcessor):
    def __init__(self):
        super(AWSInventoryProcessor, self).__init__()
        self.html_report = str()
        self.ecs = ECS()

    def generate_html_content(self, ecs_cluster_arn, ecs_cluster_name):
        logging.info(">>>>> generating content for cluster {}".format(ecs_cluster_name))
        service_details_response = self.ecs.get_service_details(ecs_cluster_arn)
        html_content = "<h2>" + ecs_cluster_name + "</h2><table><tr><th>Service</th><th>Running Count</th><th>Health</th><th>Latest Event</th></tr>"
        if not helper.is_empty_list(service_details_response['serviceArns']):
            service_arns_count = 0
            max_services_allowed_to_describe_at_once = 10
            describe_ecs_service_arns = list()
            while True:
                for ecs_service_arn in service_details_response['serviceArns']:
                    service_arns_count += 1
                    if service_arns_count <= max_services_allowed_to_describe_at_once:
                        describe_ecs_service_arns.append(ecs_service_arn)
                        if ecs_service_arn != service_details_response['serviceArns'][-1]:
                            continue
                    service_arns_count = 0
                    if not helper.is_empty_list(describe_ecs_service_arns):
                        ecs_services_details = self.ecs.describe_ecs_services(ecs_cluster_arn, describe_ecs_service_arns)
                        for ecs_service_details in ecs_services_details["services"]:
                            ecs_service_name = ecs_service_details["serviceName"]
                            running_task_count = ecs_service_details["runningCount"]
                            events = ecs_service_details["events"]
                            event_data = helper.process_events_data(events)
                            table_row = "<tr><td>"
                            if event_data["status"] == "Unsteady":
                                table_row = "<tr style=\"background: #FF0000\"><td>"
                            html_content = html_content + table_row + ecs_service_name + "</td><td>" + str(running_task_count) + "</td><td>" + event_data["status"] + "</td><td>" + \
                                           event_data["msg"] + "</td></tr>"
                        describe_ecs_service_arns = list()
                if "nextToken" in service_details_response:
                    service_details_response = self.ecs.get_paginated_service_details(ecs_cluster_arn, service_details_response["nextToken"])
                    continue
                else:
                    break
            html_content = html_content + "</table></br></br>"
            self.html_report = self.html_report + html_content
        pass

    def generate_ecs_services_health_report(self, req_cluster_name):
        ecs_cluster_arns = self.ecs.list_ecs_clusters()
        processes = []
        for ecs_cluster_arn in ecs_cluster_arns:
            ecs_cluster_name = helper.get_ecs_cluster_name_by_arn(ecs_cluster_arn)
            if not helper.is_requested_cluster(req_cluster_name, ecs_cluster_name):
                continue
            process = threading.Thread(target=self.generate_html_content, args=(ecs_cluster_arn, ecs_cluster_name,))
            processes.append(process)

        for p in processes:
            p.start()
        for p in processes:
            p.join()
        return self.html_report
