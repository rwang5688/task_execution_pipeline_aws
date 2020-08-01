import sys
import boto3
from botocore.exceptions import ClientError
import s3bucket
import s3file


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

    s3bucket.list_buckets()
    bucket = s3bucket.get_bucket(bucket_name)
    if bucket is None:
        s3bucket.create_bucket(bucket_name, region)
        bucket = s3bucket.get_bucket(bucket_name)
    s3bucket.list_buckets()

    s3file.list_files(bucket["Name"])
    s3file.upload_file(file_name, bucket["Name"])
    s3file.list_files(bucket["Name"])


if __name__ == '__main__':
    main()

