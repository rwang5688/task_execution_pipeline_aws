import logging
import boto3
from botocore.exceptions import ClientError


def get_queue_url(queue_name):
    # Create SQS client
    sqs = boto3.client('sqs')

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
    # Create SQS client
    sqs = boto3.client('sqs')

    # List SQS queues
    response = sqs.list_queues()

    # Output the bucket names
    print('\nQueueUrls:')
    if 'QueueUrls' in response:
        for queue_url in response['QueueUrls']:
            print(f'URL: {queue_url}')


def send_message(queue_url, message_body):
    # Create SQS client
    sqs = boto3.client('sqs')

    # Send message to SQS queue
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
    return response['MessageId']

def receive_message(queue_url):
    # Create SQS client
    sqs = boto3.client('sqs')

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


def delete_message(queue_url, receipt_handle):
    # Create SQS client
    sqs = boto3.client('sqs')

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

