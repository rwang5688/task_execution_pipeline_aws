import sys
import boto3
from botocore.exceptions import ClientError
import s3util


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

    s3util.list_buckets()
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        printf(f'Bucket {bucket_name} does not exist. Exit.')
        return

    s3util.list_files(bucket["Name"])
    s3util.upload_file(file_name, bucket["Name"])
    s3util.list_files(bucket["Name"])


if __name__ == '__main__':
    main()

