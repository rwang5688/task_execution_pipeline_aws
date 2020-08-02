#!/usr/bin/env python
import sys
import boto3
from botocore.exceptions import ClientError
import sqsutil
import jsonutil


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('queue_name', help='The name of the queue to send.')
    parser.add_argument('file_name', help='The name of the message file to send and receive')

    args = parser.parse_args()

    queue_name = args.queue_name
    file_name = args.file_name

    print('\nargs:')
    print(f'queue_name = {queue_name}')
    print(f'file_name = {file_name}')

    sqsutil.list_queues()
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'\nQueue {queue_name} does not exist. Exit.')
        return

    message_body = jsonutil.get_json_data(file_name)
    message_body_pretty_string = jsonutil.get_pretty_string(message_body)
    message_body_string = jsonutil.get_string(message_body)
    message_id = sqsutil.send_message(queue_url, message_body_string)
    print('\nMessageBody: (in pretty print)')
    print(message_body_pretty_string)
    print(f'MessageId: {message_id}')

    message = sqsutil.receive_message(queue_url)
    if message is not None:
        receipt_handle = message['ReceiptHandle']
        sqsutil.delete_message(queue_url, receipt_handle)
    print('\nReceived and deleted message:')
    print(jsonutil.get_pretty_string(message))


if __name__ == '__main__':
    main()

