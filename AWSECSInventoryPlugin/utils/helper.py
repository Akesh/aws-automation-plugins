def get_ecs_cluster_name_by_arn(ecs_cluster_arn):
    return ecs_cluster_arn.split("/")[1]


def is_requested_cluster(req_cluster_name, ecs_cluster_name):
    if req_cluster_name and req_cluster_name.upper() != ecs_cluster_name.upper():
        return False
    return True


def is_empty_list(list):
    if len(list) > 0:
        return False
    return True


def process_events_data(events):
    latest_event_msg = ''
    status = ''
    event_data = dict()
    if events:
        latest_event_msg = events[0]['message']
        if "steady" in latest_event_msg:
            status = "Steady"
            latest_event_msg = "-"
        else:
            status = "Unsteady"
    event_data['status'] = status
    event_data['msg'] = latest_event_msg
    return event_data
