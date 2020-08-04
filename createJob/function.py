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
import jobstable


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


def send_message(queue_name, item):
    # get queue url
    sqsutil.list_queues()
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'\nQueue {queue_name} does not exist.')
        return False

    # send message
    message_body = {
        "action": "process",
        "job": {
            "id": item['id'],
            "tool": item['tool'],
            "source": item['source']
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


# handler
def createJob(event, context):
    success = preamble(event, context)
    if not success:
        print('preamble failed. Exit.')
        return False

    # get jobs table
    jobs_table = jobstable.get_jobs_table()
    if jobs_table is None:
        return False

    # create jobs record
    event_records = event['Records']
    for event_record in event_records:
        print('\nEvent Record:')
        print(event_record)

        # create job record
        job_id = jobstable.create_job_record(jobs_table, event_record)
        if job_id is None:
            print('create_job_record failed.  Exit')
            return False
        item = jobstable.get_job_record(jobs_table, job_id)
        if item is None:
            print('get_job_record failed.  Exit')
            return False
        print('\nCreated Job Record:')
        print(item)

        # if environment variable exists, use it
        queue_name = 'jobs-list-process-job-queue-rwang5688'
        if 'JOBS_LIST_PROCESS_QUEUE' in os.environ:
            queue_name = os.environ['JOBS_LIST_PROCESS_JOB_QUEUE']
        send_message(queue_name, item)

        # update job status
        success = jobstable.update_job_status(jobs_table, job_id, "started", "")

    # successfully processed all records
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

