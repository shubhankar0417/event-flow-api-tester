import os
from dotenv import load_dotenv


def get_config():    
    # Load the .env file
    load_dotenv()
    return {
        'GUARDIAN_API_KEY':os.getenv('GUARDIAN_API_KEY'),
        'GUARDIAN_API_URL':os.getenv('GUARDIAN_API_URL'),
        'SQS_QUEUE_URL':os.getenv('SQS_QUEUE_URL'),
        'CATEGORY':os.getenv('CATEGORY'),
        'AWS_REGION_NAME':os.getenv('AWS_REGION_NAME'),
        'AWS_ACCESS_KEY':os.getenv('AWS_ACCESS_KEY'),
        'AWS_SECRET_ACCESS_KEY':os.getenv('AWS_SECRET_ACCESS_KEY'),
        'LAMBDA_LOG_GROUP':os.getenv('LAMBDA_LOG_GROUP'),
        'LAMBDA_SUCCESS_MSG':os.getenv('LAMBDA_SUCCESS_MSG'),
        'BUCKET_NAME':os.getenv('BUCKET_NAME'),
        'PREFIX':os.getenv('PREFIX')
    }