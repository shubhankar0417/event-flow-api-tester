import boto3
from utils.config import get_config


def check_lambda_logs_in_cloud_watch():
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
        return False, None, None
    
    stream_name = streams['logStreams'][0]['logStreamName']

    # Fetch the latest logs from that stream
    logs = cloud_watch_client.get_log_events(
        logGroupName=config['LAMBDA_LOG_GROUP'],
        logStreamName=stream_name,
        limit=50,
        startFromHead=False
    )

    sqs_success_message = None
    s3_success_message = None
    for event in reversed(logs['events']):
        if config['LAMBDA_SUCCESS_MSG'] in event.get('message'):
            sqs_success_message = event.get('message')
        if 'Successfully uploaded filtered data to s3://' in event.get('message'):
            s3_success_message = event.get('message')
    
    print('Found SQS success message :', sqs_success_message)
    print('Found S3 success message :', s3_success_message)

    if bool(sqs_success_message and s3_success_message):
        return True, sqs_success_message, s3_success_message    

    return False, sqs_success_message, s3_success_message