import boto3
import json
from utils.config import get_config


def send_message_to_sqs(message):
    config = get_config()
    sqs_client = boto3.client('sqs',
                               region_name=config['AWS_REGION_NAME'],
                               aws_access_key_id=config['AWS_ACCESS_KEY'],
                               aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])
    sqs_response = sqs_client.send_message(
        QueueUrl = config['SQS_QUEUE_URL'],
        MessageBody=json.dumps(message)
    )
    return sqs_response