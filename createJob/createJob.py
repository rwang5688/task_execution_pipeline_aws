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
        print(f'send_message: Queue {queue_name} does not exist.')
        return False

    # send message
    message_body = {
        "action": "process",
        "job": {
            "job_id": item['job_id'],
            "job_tool": item['job_tool'],
            "job_source": item['job_source']
        }
    }
    message_id = sqsutil.send_message(queue_url, str(message_body))
    print(f'MessageId: {message_id}')
    print(f'MessageBody: {message_body}')

    # debug: receive message
    message = sqsutil.receive_message(queue_url)
    if message is None:
        print(f'send_message: cannot retrieve sent messge.')
        return False
    print('Received message:')
    print(message)

    # success
    return True


# createJob handler
def createJob(event, context):
    success = preamble(event, context)
    if not success:
        print('preamble failed. Exit.')
        return False

    # get jobs table
    jobs_table = jobstable.get_jobs_table()
    if jobs_table is None:
        print('get_jobs_table failed.  Exit.')
        return False

    # create jobs record
    event_records = event['Records']
    for event_record in event_records:
        # debug: print event record
        print('Event Record:')
        print(event_record)

        # create job record
        job_id = jobstable.create_job_record(jobs_table, event_record)
        if job_id is None:
            print('create_job_record failed.  Exit')
            return False

        # debug: get and print job record
        item = jobstable.get_job_record(jobs_table, job_id)
        if item is None:
            print('get_job_record failed.  Exit')
            return False
        print('Job Record:')
        print(item)

        # set process job queue name
        queue_name = 'jobs-list-process-job-queue-rwang5688'
        if 'PROCESS_JOB_QUEUE' in os.environ:
            queue_name = os.environ['PROCESS_JOB_QUEUE']

        # send job context to process job queue
        success = send_message(queue_name, item)
        if not success:
            print('send_message failed.  Exit.')
            return False

        # TO DO:
        # Start ECS task to process job!!!

        # update job status
        job_status = "started"
        job_logfile = ""
        success = jobstable.update_job_status(jobs_table, job_id, job_status, job_logfile)

    # successfully processed all records
    return True


# main function for testing createJob handler
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

