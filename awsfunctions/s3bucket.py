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
    print('\nExisting buckets:')
    if 'Buckets' in response:
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')

