from utils.config import get_config
import boto3

def get_latest_file_from_s3(fail_on_purpose=False):
    if fail_on_purpose:
        return 'File not found'
    config = get_config()
    s3_client = boto3.client('s3',
                            region_name=config['AWS_REGION_NAME'],
                            aws_access_key_id=config['AWS_ACCESS_KEY'],
                            aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])
    bucket_list = s3_client.list_objects_v2(
        Bucket=config['BUCKET_NAME'],
        Prefix=config['PREFIX']
    )
    latest_file_name = bucket_list['Contents'][-1]['Key']
    return latest_file_name