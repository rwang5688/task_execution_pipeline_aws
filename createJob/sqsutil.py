import os
import logging
import boto3
from botocore.exceptions import ClientError


def get_sqs_client():
    aws_access_key_id = ''
    if 'AWS_ACCESS_KEY_ID' in os.environ:
        aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = ''
    if 'AWS_SECRET_ACCESS_KEY' in os.environ:
        aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    region_name = 'us-west-2'
    if 'AWS_DEFAULT_REGION' in os.environ:
        region_name = os.environ['AWS_DEFAULT_REGION']

    #print(f'aws_access_key_id={aws_access_key_id}')
    #print(f'aws_secret_access_key={aws_secret_access_key}')
    #print(f'region_name={region_name}')

    sqs = boto3.client('sqs',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
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

