import os
import logging
import boto3
from botocore.exceptions import ClientError


def get_s3_client():
    region_name = ''
    if 'TARGET_REGION' in os.environ:
        region_name = os.environ['TARGET_REGION']
    print('get_s3_client: region_name=%s' % region_name)

    session = boto3.Session(profile_name=None)
    s3 = session.client('s3',
        region_name=region_name)
    return s3


def list_buckets():
    # Retrieve the list of existing buckets
    s3 = get_s3_client()
    response = s3.list_buckets()

    # Print bucket names
    print('\nBuckets:')
    if 'Buckets' in response:
        for bucket in response['Buckets']:
            print('Name: %s' % bucket["Name"])


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


def get_file_object(bucket_name, object_name):
    s3 = get_s3_client()
    result = None

    try:
        result = s3.get_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        logging.error(e)
        return None

    return result


def list_files(bucket_name):
    # Retrieve the list of existing files
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Print bucket name and object keys
    print('\nBucket: %s' % response["Name"])
    print('Contents:')
    if 'Contents' in response:
        for bucketFile in response['Contents']:
            print('Key: %s' % bucketFile["Key"])


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    s3 = get_s3_client()
    try:
        response = s3.upload_file(file_name, bucket, object_name)
        print('s3util.upload_file: response=%s' % response)
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
        print('s3util.download_file: response=%s' % response)
    except ClientError as e:
        logging.error(e)
        return False
    return True

