#!/usr/bin/env python
import boto3
from botocore.exceptions import ClientError
import sqsutil
import jsonutil


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', help='The name of the message file to send and receive')
    parser.add_argument('queue_name', help='The name of the queue to send.')

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

    # test pretty string: this is not used for sending
    message_body_pretty_string = jsonutil.get_pretty_string(message_body)
    print('\nMessageBody: (pretty string)')
    print(message_body_pretty_string)

    # test string: this is not used for sending
    message_body_string = jsonutil.get_string(message_body)
    print('\nMessageBody: (string)')
    print(message_body_string)

    # use str(message_body) for sending
    message_id = sqsutil.send_message(queue_url, str(message_body))
    print(f'MessageId: {message_id}')
    print(f'MessageBody: {message_body}')

    message = sqsutil.receive_message(queue_url)
    success = sqsutil.delete_message(queue_url, message)
    if not success:
        print('\ndelete_message failed.  Exit.')
        return
    print('\nReceived and deleted message:')
    print(message)


if __name__ == '__main__':
    main()

