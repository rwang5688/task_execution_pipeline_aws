#!/usr/bin/env python
import boto3
from botocore.exceptions import ClientError
import s3util
import sqsutil


def parse_arguments():
    import argparse
    global tool_name
    global source_name
    global bucket_name
    global queue_name

    parser = argparse.ArgumentParser()
    parser.add_argument('tool_name', help='The name of the tool to run.')
    parser.add_argument('source_name', help='The name of the source package to run.')
    parser.add_argument('bucket_name', help='The name of the bucket to upload source.')
    parser.add_argument('queue_name', help='The name of the queue to send message.')

    args = parser.parse_args()
    tool_name = args.tool_name
    source_name = args.source_name
    bucket_name = args.bucket_name
    queue_name = args.queue_name

    if tool_name is None:
        print('parse_arguments: tool_name is missing.')
        return False

    if source_name is None:
        print('parse_arguments: source_name is missing.')
        return False

    if bucket_name is None:
        print('parse_arguments: bucket_name is missing.')
        return False

    if queue_name is None:
        print('parse_arguments: queue_name is missing.')
        return False

    # success
    return True


def upload_source(bucket_name, source_name):
    # get bucket
    s3util.list_buckets()
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        printf(f'upload_source: Bucket {bucket_name} does not exist.')
        return False

    # upload file
    s3util.list_files(bucket["Name"])
    success = s3util.upload_file(source_name, bucket["Name"])
    if not success:
        printf(f'upload_source: Failed to upload source file {source_name}.')
        return False
    s3util.list_files(bucket["Name"])

    # successfully uploaded file
    return True


def send_message(queue_name, tool_name, source_name):
    # get queue url
    sqsutil.list_queues()
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'send_message: Queue {queue_name} does not exist.')
        return False

    # send message
    message_body = {
        "action": "submit",
        "job": {
            "tool": tool_name,
            "source": source_name
        }
    }
    message_id = sqsutil.send_message(queue_url, str(message_body))
    print(f'MessageId: {message_id}')
    print(f'MessageBody: {message_body}')

    # receive message
    message = sqsutil.receive_message(queue_url)
    print('\nReceived message:')
    print(message)

    # successfully sent and received message
    return True


def main():
    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('\nargs:')
    print(f'tool_name = {tool_name}')
    print(f'source_name = {source_name}')
    print(f'bucket_name = {bucket_name}')
    print(f'queue_name = {queue_name}')

    success = upload_source(bucket_name, source_name)
    if not success:
        print('upload_source failed.  Exit.')
        return

    success = send_message(queue_name, tool_name, source_name)
    if not success:
        print('upload_source failed.  Exit.')
        return


if __name__ == '__main__':
    main()

