import os
import logging
import boto3
from botocore.exceptions import ClientError


def get_sqs_client():
    region_name = ''
    if 'TARGET_REGION' in os.environ:
        region_name = os.environ['TARGET_REGION']
    print(f'get_sqs_client: region_name={region_name}')

    session = boto3.Session(profile_name='aws-admin')
    sqs = session.client('sqs',
        region_name=region_name)
    return sqs


def get_queue_url(queue_name):
    sqs = get_sqs_client()

    # Make sure queue name exists
    response = sqs.list_queues()

    # Get URL for SQS queue
    try:
        response = sqs.get_queue_url(QueueName=queue_name)
    except ClientError as e:
        logging.error(e)
        return None

    return response['QueueUrl']


def list_queues():
    sqs = get_sqs_client()

    # List SQS queues
    response = sqs.list_queues()

    # Output the bucket names
    print('\nQueueUrls:')
    if 'QueueUrls' in response:
        for queue_url in response['QueueUrls']:
            print(f'URL: {queue_url}')


def send_message(queue_url, message_body):
    sqs = get_sqs_client()

    # Send message to SQS queue
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
    return response['MessageId']


def receive_message(queue_url):
    sqs = get_sqs_client()

    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SenderId',
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    message = None
    if 'Messages' in response:
        message = response['Messages'][0]
    return message


def delete_message(queue_url, message):
    sqs = get_sqs_client()

    # Get receipt handle
    if message is None:
        print('delete_message: message is None.  No receipt handle.')
        return False
    receipt_handle = message['ReceiptHandle']

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

    return True

