#!/usr/bin/env python
import os
import subprocess
import boto3
from botocore.exceptions import ClientError
import s3util
import sqsutil


def parse_arguments():
    import argparse
    global job_id
    global job_status
    global logfile_name

    parser = argparse.ArgumentParser()
    parser.add_argument('job_id', help='The id of the job to update.')
    parser.add_argument('job_status', help='The status of the job to update.')
    parser.add_argument('logfile_name', help='The name of the log file to update.')

    args = parser.parse_args()
    job_id = args.job_id
    job_status = args.job_status
    logfile_name = args.logfile_name

    if job_id is None:
        print('parse_arguments: job_id is missing.')
        return False

    if job_status is None:
        print('parse_arguments: job_status is missing.')
        return False

    if logfile_name is None:
        print('parse_arguments: logfile_name is missing.')
        return False

    # success
    return True


def get_env_vars():
    global bucket_name
    global queue_name

    bucket_name = 'jobs-list-log-data-bucket-rwang5688'
    if 'JOBS_LIST_LOG_DATA_BUCKET' in os.environ:
        bucket_name = os.environ['JOBS_LIST_LOG_DATA_BUCKET']

    queue_name = 'jobs-list-update-job-queue-rwang5688'
    if 'JOBS_LIST_UPDATE_JOB_QUEUE' in os.environ:
        queue_name = os.environ['JOBS_LIST_UPDATE_JOB_QUEUE']

    # successfully got environment variables
    return True


def upload_logfile(bucket_name, logfile_name):
    # get bucket
    s3util.list_buckets()
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        printf(f'upload_log: Bucket {bucket_name} does not exist.')
        return False

    # upload file
    s3util.list_files(bucket["Name"])
    success = s3util.upload_file(logfile_name, bucket["Name"])
    if not success:
        printf(f'upload_log: Failed to upload log file {logfile_name}.')
        return False
    s3util.list_files(bucket["Name"])

    # successfully uploaded file
    return True


def send_message(queue_name, job_id, job_status, logfile_name):
    # get queue url
    sqsutil.list_queues()
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'send_message: Queue {queue_name} does not exist.')
        return False

    # send message
    message_body = {
        "action": "update",
        "job": {
            "id": job_id,
            "job_status": job_status,
            "logfile": logfile_name
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
    print('\nStarting jobLog.py ...')

    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('\nargs:')
    print(f'job_id = {job_id}')
    print(f'job_status = {job_status}')
    print(f'logfile_name = {logfile_name}')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('\nEnv vars:')
    print(f'bucket_name: {bucket_name}')
    print(f'queue_name: {queue_name}')

    success = upload_logfile(bucket_name, logfile_name)
    if not success:
        print('upload_logfile failed.  Exit.')
        return

    success = send_message(queue_name, job_id, job_status, logfile_name)
    if not success:
        print('upload_log failed.  Exit.')
        return


if __name__ == '__main__':
    main()

