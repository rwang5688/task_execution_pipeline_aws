import os
import logging
import boto3
from botocore.exceptions import ClientError


def get_s3_client():
    region_name = ''
    if 'TARGET_REGION' in os.environ:
        region_name = os.environ['TARGET_REGION']
    print(f'get_s3_client: region_name={region_name}')

    session = boto3.Session(profile_name='aws-admin')
    s3 = session.client('s3',
        region_name=region_name)
    return s3


def list_buckets():
    # Retrieve the list of existing buckets
    s3 = get_s3_client()
    response = s3.list_buckets()

    # Output the bucket names
    print('\nBuckets:')
    if 'Buckets' in response:
        for bucket in response['Buckets']:
            print(f'Name: {bucket["Name"]}')


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

