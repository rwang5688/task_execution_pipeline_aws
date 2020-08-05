import logging
import boto3
from botocore.exceptions import ClientError


def get_bucket(bucket_name):
    # Retrieve the list of existing buckets
    s3 = boto3.client('s3')
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
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    # Output the bucket names
    print('\nBuckets:')
    if 'Buckets' in response:
        for bucket in response['Buckets']:
            print(f'Name: {bucket["Name"]}')


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(bucket_name, object_name, file_name=None):
    if file_name is None:
        file_name = object_name

    s3 = boto3.client('s3')
    try:
        response = s3.download_file(bucket_name, object_name, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def list_files(bucket_name):
    # Retrieve the list of existing files
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Output the bucket names
    print(f'\nBucket: {response["Name"]}')
    print('Contents:')
    if 'Contents' in response:
        for bucketFile in response['Contents']:
            print(f'Key: {bucketFile["Key"]}')

