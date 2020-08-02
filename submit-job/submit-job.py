#!/usr/bin/env python
import sys
import boto3
from botocore.exceptions import ClientError
import json
import s3util
import sqsutil
import jsonutil


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('source_name', help='The name of the source file to upload')
    parser.add_argument('bucket_name', help='The name of the bucket to upload file.')
    parser.add_argument('queue_name', help='The name of the queue to send message')

    args = parser.parse_args()

    source_name = args.source_name
    bucket_name = args.bucket_name
    queue_name = args.queue_name

    print('\nargs:')
    print(f'source_name = {source_name}')
    print(f'bucket_name = {bucket_name}')
    print(f'queue_name = {queue_name}')

    # get bucket
    s3util.list_buckets()
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        printf(f'Bucket {bucket_name} does not exist. Exit.')
        return

    # upload file
    s3util.list_files(bucket["Name"])
    okay = s3util.upload_file(source_name, bucket["Name"])
    if not okay:
        printf(f'Failed to upload source file: {source_name}.  Exit.')
        return
    s3util.list_files(bucket["Name"])

    # get queue url
    sqsutil.list_queues()
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'\nQueue {queue_name} does not exist. Exit.')
        return

    # create message body strings
    message_body = {'action': 'submit', 'job': {'source': source_name}}
    message_body_pretty_string = jsonutil.get_pretty_string(message_body)
    message_body_string = jsonutil.get_string(message_body)
    print('\nMessageBody: (in pretty print)')
    print(message_body_pretty_string)
    print('\nMessageBody: (in single line)')
    print(message_body_string)

    # send message
    message_id = sqsutil.send_message(queue_url, message_body_string)
    print(f'MessageId: {message_id}')

    # receive message
    message = sqsutil.receive_message(queue_url)
    print('\nReview message:')
    print(jsonutil.get_pretty_string(message))


if __name__ == '__main__':
    main()

