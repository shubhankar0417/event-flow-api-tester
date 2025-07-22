import pytest
import time
from utils.config import get_config
from aws_pipeline.guardian.articles import get_guardian_articles
from aws_pipeline.sqs.sqs_handler import send_message_to_sqs
from aws_pipeline.lambda_aws.lambda_handler import check_lambda_logs_in_cloud_watch
from aws_pipeline.s3.s3_handler import get_latest_file_from_s3

def test_full_event_flow():
    config = get_config()

    # take the returned response from fetch guardian article function
    guardian_api_response = get_guardian_articles(config['CATEGORY'])
    assert guardian_api_response.status_code == 200, (
        f'Guaradian API failed: {guardian_api_response.status_code}\n Response text: {guardian_api_response.text}'
    )
    print('1. Success - GET API PASSED')
 
    # Send the data to the SQS queue
    message = guardian_api_response.json()
    sqs_response = send_message_to_sqs(message)
    sqs_response_status = sqs_response['ResponseMetadata']['HTTPStatusCode']
    assert sqs_response_status == 200, (
        f'SQS message sending failed: {sqs_response_status}'
    )
    print('2. Success - SQS MESSAGE PASSED')

    # verify lambda is triggered from sqs 
    time.sleep(10)
    lambda_status, sqs_success_message, s3_success_message = check_lambda_logs_in_cloud_watch()
    assert lambda_status == True, ('Lambda could not process SQS message properly')
    print('3. Success - LAMBDA FUNCTION PASSED')

    # verify if the filtered data is uploaded to S3 or not
    latest_s3_uploaded_file = get_latest_file_from_s3()
    assert latest_s3_uploaded_file in s3_success_message, ('S3 file not uploaded successfully')
    print('4. Success - S3 FILE UPLOAD PASSED')
