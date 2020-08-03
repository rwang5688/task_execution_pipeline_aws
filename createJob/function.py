#!/usr/bin/env python
import os
import logging
import jsonpickle
import boto3
from botocore.exceptions import ClientError
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import s3util
import sqsutil
import jobstableutil


logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()


def preamble(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))
    client = boto3.client('lambda')
    account_settings = client.get_account_settings()
    print(account_settings['AccountUsage'])
    return True


def send_message(queue_name, job_id, source_name):
    # get queue url
    sqsutil.list_queues()
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'\nQueue {queue_name} does not exist.')
        return False

    # send message
    message_body = {"action": "process", "job": {"id": job_id, "source": source_name}}
    message_id = sqsutil.send_message(queue_url, str(message_body))
    print(f'MessageId: {message_id}')
    print(f'MessageBody: {message_body}')

    # receive message
    message = sqsutil.receive_message(queue_url)
    print('\nReceived message:')
    print(message)

    # successfully sent and received message
    return True


# handler
def createJob(event, context):
    success = preamble(event, context)
    if not success:
        print('preamble failed. Exit.')
        return False

    # get jobs table
    jobs_table = jobstableutil.get_jobs_table()

    # create jobs record
    event_records = event['Records']
    for event_record in event_records:
        print('\nEvent Record:')
        print(event_record)

        # create job record
        job_id = jobstableutil.create_job_record(jobs_table, event_record)
        item = jobstableutil.get_job_record(jobs_table, job_id)
        if item is None:
            print('create_job_record failed.  Exit')
            return False
        print('\nCreated Job Record:')
        print(item)

        # send message
        # ... hard code queue name for now
        queue_name = 'jobs-list-process-job-queue-rwang5688'
        job_id = item['id']
        source_name = item['source']
        send_message(queue_name, job_id, source_name)

        # update job status
        success = jobstableutil.update_job_status(jobs_table, job_id, "started")

    return True


# main function for testing and debugging handler
def main():
    xray_recorder.begin_segment('main_function')
    file = open('event.json', 'rb')
    try:
        # read sample event
        ba = bytearray(file.read())
        event = jsonpickle.decode(ba)
        logger.warning('## EVENT')
        logger.warning(jsonpickle.encode(event))
        # create sample context
        context = {'requestid': '1234'}
        # invoke handler
        result = createJob(event, context)
        # print response
        print('## RESPONSE')
        print(str(result))
    finally:
        file.close()
    file.close()
    xray_recorder.end_segment()


if __name__ == '__main__':
    main()

