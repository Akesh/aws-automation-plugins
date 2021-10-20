import logging

import boto3

cwlogs_client = boto3.client('logs')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

HTML_CONTENT_START = "<!DOCTYPE><html><head><title>CloudWatch Report</title><style>table{font-family:arial,sans-serif;border:1px solid #dddddd;width:100%;} h2{font-family:arial,sans-serif;width:100%;text-align:center;} h3{font-family:arial,sans-serif;width:100%;padding-left:25%;} td,th{border:1px solid #dddddd;text-align:left; padding:8px;} tr:nth-child(even){background-color:#dddddd;}</style></head><body>"
HTML_CONTENT_END = "</body></html>"


def bytes_to_human_readable(number_of_bytes):
    if number_of_bytes < 0:
        raise ValueError("!!! number_of_bytes can't be smaller than 0 !!!")

    step_to_greater_unit = 1024.

    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'KB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'MB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'GB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'TB'

    precision = 1
    number_of_bytes = round(number_of_bytes, precision)

    return str(number_of_bytes) + ' ' + unit


def get_cloudwatch_data(event, context):
    logger.info("Event {}".format(event))
    cwlogs_list_response = cwlogs_client.describe_log_groups()
    if cwlogs_list_response['logGroups']:
        html_content = "<table><tr><th>Log Group</th><th>Data Size</th>"
        while True:
            for cwlog_group in cwlogs_list_response['logGroups']:
                log_group_name = cwlog_group["logGroupName"]
                log_group_data_size = bytes_to_human_readable(cwlog_group["storedBytes"])
                table_row = "<tr><td>"
                if "GB" in log_group_data_size or "TB" in log_group_data_size:
                    table_row = '<tr style="background: #FF0000"><td>'
                html_content += table_row + log_group_name + "</td><td>" + log_group_data_size + "</td></tr>"
            if "nextToken" in cwlogs_list_response:
                cwlogs_list_response = cwlogs_client.describe_log_groups(nextToken=cwlogs_list_response['nextToken'])
                continue
            else:
                break
    return HTML_CONTENT_START + html_content + HTML_CONTENT_END
