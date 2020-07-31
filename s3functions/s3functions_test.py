import sys
import boto3
from botocore.exceptions import ClientError
from s3bucket import *
from s3file import *


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('bucket_name', help='The name of the bucket to create.')
    parser.add_argument('region', help='The region in which to create your bucket.')
    parser.add_argument('file_name', help='The name of the file to upload')

    args = parser.parse_args()

    bucket_name = args.bucket_name
    region = args.region
    file_name = args.file_name

    print(f'bucket_name = {bucket_name}')
    print(f'region = {region}')
    print(f'file_name = {file_name}')

    list_buckets()
    bucket = get_bucket(bucket_name)
    if bucket is None:
        create_bucket(bucket_name, region)
        bucket = get_bucket(bucket_name)
    list_buckets()

    list_files(bucket["Name"])
    upload_file(file_name, bucket["Name"])
    list_files(bucket["Name"])


if __name__ == '__main__':
    main()

