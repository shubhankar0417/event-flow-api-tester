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
        f'1. Failure - GET API FAILED: {guardian_api_response.status_code}'
    )
    print('1. Success - GET API PASSED')
 
    # Send the data to the SQS queue
    message = guardian_api_response.json()
    sqs_response = send_message_to_sqs(message)
    sqs_response_status = sqs_response['ResponseMetadata']['HTTPStatusCode']
    assert sqs_response_status == 200, (
        f'2. Failure - SQS QUEUE FAILED: {sqs_response_status}'
    )
    print('2. Success - SQS QUEUE PASSED')

    # verify lambda is triggered from sqs 
    time.sleep(10)
    lambda_status, sqs_message, s3_message = check_lambda_logs_in_cloud_watch(fail_on_purpose=False)
    assert lambda_status == True, (f'3. Failure - LAMBDA FUNCTION FAILED:\nSQS:{sqs_message}\nS3:{s3_message}')
    print('3. Success - LAMBDA FUNCTION PASSED')

    # verify if the filtered data is uploaded to S3 or not
    latest_s3_uploaded_file = get_latest_file_from_s3(fail_on_purpose=False)
    assert latest_s3_uploaded_file in s3_message, (f'4. Failure - S3 FILE UPLOAD FAILED: {latest_s3_uploaded_file}')
    print('4. Success - S3 FILE UPLOAD PASSED')

def test_simulate_lambda_service_failure():
    config = get_config()

    # take the returned response from fetch guardian article function
    guardian_api_response = get_guardian_articles(config['CATEGORY'])
    assert guardian_api_response.status_code == 200, (
        f'1. Failure - GET API FAILED: {guardian_api_response.status_code}'
    )
    print('1. Success - GET API PASSED')
 
    # Send the data to the SQS queue
    message = guardian_api_response.json()
    sqs_response = send_message_to_sqs(message)
    sqs_response_status = sqs_response['ResponseMetadata']['HTTPStatusCode']
    assert sqs_response_status == 200, (
        f'2. Failure - SQS QUEUE FAILED: {sqs_response_status}'
    )
    print('2. Success - SQS QUEUE PASSED')

    # verify lambda is triggered from sqs 
    time.sleep(10)
    lambda_status, sqs_message, s3_message = check_lambda_logs_in_cloud_watch(fail_on_purpose=True)
    assert lambda_status == True, (f'3. Failure - LAMBDA FUNCTION FAILED:\nSQS:{sqs_message}\nS3:{s3_message}')
    print('3. Success - LAMBDA FUNCTION PASSED')

    # verify if the filtered data is uploaded to S3 or not
    latest_s3_uploaded_file = get_latest_file_from_s3(fail_on_purpose=False)
    assert latest_s3_uploaded_file in s3_message, (f'4. Failure - S3 FILE UPLOAD FAILED: {latest_s3_uploaded_file}')
    print('4. Success - S3 FILE UPLOAD PASSED')

def test_simulate_s3_service_failure():
    config = get_config()

    # take the returned response from fetch guardian article function
    guardian_api_response = get_guardian_articles(config['CATEGORY'])
    assert guardian_api_response.status_code == 200, (
        f'1. Failure - GET API FAILED: {guardian_api_response.status_code}'
    )
    print('1. Success - GET API PASSED')
 
    # Send the data to the SQS queue
    message = guardian_api_response.json()
    sqs_response = send_message_to_sqs(message)
    sqs_response_status = sqs_response['ResponseMetadata']['HTTPStatusCode']
    assert sqs_response_status == 200, (
        f'2. Failure - SQS QUEUE FAILED: {sqs_response_status}'
    )
    print('2. Success - SQS QUEUE PASSED')

    # verify lambda is triggered from sqs 
    time.sleep(10)
    lambda_status, sqs_message, s3_message = check_lambda_logs_in_cloud_watch(fail_on_purpose=False)
    assert lambda_status == True, (f'3. Failure - LAMBDA FUNCTION FAILED:\nSQS:{sqs_message}\nS3:{s3_message}')
    print('3. Success - LAMBDA FUNCTION PASSED')

    # verify if the filtered data is uploaded to S3 or not
    latest_s3_uploaded_file = get_latest_file_from_s3(fail_on_purpose=True)
    assert latest_s3_uploaded_file in s3_message, (f'4. Failure - S3 FILE UPLOAD FAILED: {latest_s3_uploaded_file}')
    print('4. Success - S3 FILE UPLOAD PASSED')
  