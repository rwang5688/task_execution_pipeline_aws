import os
import logging
import boto3
from botocore.exceptions import ClientError


def get_s3_client():
    aws_access_key_id = "AKIA2GJJEXXSJZPSMU6C"
    if 'AWS_ACCESS_KEY' in os.environ:
        aws_access_key_id = os.environ['AWS_ACCESS_KEY']
    aws_secret_access_key = "1X7F/mP2yebPYWbeueJg4ZREZF+yGZKafUe/1iS5"
    if 'AWS_SECRET_ACCESS_KEY' in os.environ:
        aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    region_name = 'us-west-2'
    if 'AWS_DEFAULT_REGION' in os.environ:
        region_name = os.environ['AWS_DEFAULT_REGION']

    print(f'region_name={region_name}')
    print(f'aws_access_key_id={aws_access_key_id}')
    print(f'aws_secret_access_key={aws_secret_access_key}')

    s3 = boto3.client('s3',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
        region_name=region_name)
    return s3


def get_bucket(bucket_name):
    # Retrieve the list of existing buckets
    s3 = get_s3_client()
    response = s3.list_buckets()

    # Find the bucket by name
    result = None
    for bucket in response['Buckets']:
        if bucket["Name"] == bucket_name:
            result = bucket
            break

    return result


def list_buckets():
    # Retrieve the list of existing buckets
    s3 = get_s3_client()
    response = s3.list_buckets()

    # Output the bucket names
    print('\nBuckets:')
    if 'Buckets' in response:
        for bucket in response['Buckets']:
            print(f'Name: {bucket["Name"]}')


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    s3 = get_s3_client()
    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(bucket_name, object_name, file_name=None):
    if file_name is None:
        file_name = object_name

    s3 = get_s3_client()
    try:
        response = s3.download_file(bucket_name, object_name, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def list_files(bucket_name):
    # Retrieve the list of existing files
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Output the bucket names
    print(f'\nBucket: {response["Name"]}')
    print('Contents:')
    if 'Contents' in response:
        for bucketFile in response['Contents']:
            print(f'Key: {bucketFile["Key"]}')

