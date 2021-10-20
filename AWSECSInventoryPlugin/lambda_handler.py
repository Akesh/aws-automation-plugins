import logging

from processors.aws_inventory_processor import AWSInventoryProcessor

logger = logging.getLogger()
logger.setLevel(logging.INFO)

HTML_CONTENT_START = "<!DOCTYPE><html><head><title>ECS Service Health Report</title><style>table{font-family:arial,sans-serif;border:1px solid #dddddd;width:100%;} h2{font-family:arial,sans-serif;width:100%;text-align:center;} h3{font-family:arial,sans-serif;width:100%;padding-left:25%;} td,th{border:1px solid #dddddd;text-align:left; padding:8px; width:25%} tr:nth-child(even){background-color:#dddddd;}</style></head><body>"
HTML_CONTENT_END = "</body></html>"


def generate_health_report(event, context):
    logger.info('got event {}'.format(event))
    cluster_name = event["cluster"]
    aws_inventory_processor = AWSInventoryProcessor()
    html_content = aws_inventory_processor.generate_ecs_services_health_report(cluster_name)
    print(HTML_CONTENT_START + html_content + HTML_CONTENT_END)
    return HTML_CONTENT_START + html_content + HTML_CONTENT_END
