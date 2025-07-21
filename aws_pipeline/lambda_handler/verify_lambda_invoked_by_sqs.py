import boto3
from utils.config import get_config


def get_latest_lambda_log_and_check_successful_processing():
    config = get_config()
    cloud_watch_client = boto3.client('logs',
                                    region_name=config['AWS_REGION_NAME'],
                                    aws_access_key_id=config['AWS_ACCESS_KEY'],
                                    aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])
    streams = cloud_watch_client.describe_log_streams(
        logGroupName=config['LAMBDA_LOG_GROUP'],
        orderBy='LastEventTime',
        descending=True,
        limit=1
    )
    # print('Streams :', streams)
    if not streams['logStreams']:
        return False
    
    stream_name = streams['logStreams'][0]['logStreamName']

    # Fetch the latest logs from that stream
    logs = cloud_watch_client.get_log_events(
        logGroupName=config['LAMBDA_LOG_GROUP'],
        logStreamName=stream_name,
        limit=50,
        startFromHead=False
    )

    # print('Logs :', logs)
    sqs_success_message = None
    s3_success_message = None
    for event in logs.get('events', []):
        # print('Events :', event)
        if config['LAMBDA_SUCCESS_MSG'] in event.get('message'):
            sqs_success_message = event.get('message')
        if 'Successfully uploaded filtered data to s3://' in event.get('message'):
            s3_success_message = event.get('message')

        """if config['LAMBDA_SUCCESS_MSG'] in event.get("message", ""):
            print('Lambda success message : ', event['message'])
            return True"""
    if bool(sqs_success_message and s3_success_message):
        return True, sqs_success_message, s3_success_message    

    return False, sqs_success_message, s3_success_message