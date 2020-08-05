#!/usr/bin/env python
import os
import subprocess
import boto3
from botocore.exceptions import ClientError
import s3util
import sqsutil


def get_env_vars():
    global bucket_name
    global queue_name

    bucket_name = 'jobs-list-source-data-bucket-rwang5688'
    if 'JOBS_LIST_SOURCE_DATA_BUCKET' in os.environ:
        bucket_name = os.environ['JOBS_LIST_SOURCE_DATA_BUCKET']

    queue_name = 'jobs-list-process-job-queue-rwang5688'
    if 'JOBS_LIST_PROCESS_JOB_QUEUE' in os.environ:
        queue_name = os.environ['JOBS_LIST_PROCESS_JOB_QUEUE']

    # successfully got environment variables
    return True


def receive_message(queue_name):
    # get queue url
    sqsutil.list_queues()
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'\nQueue {queue_name} does not exist.')
        return False

    # receive message
    message = sqsutil.receive_message(queue_url)
    print('\nReceived message:')
    print(message)

    # successfully received message
    return message


def parse_message(message):
    global job_id
    global source_name
    global tool_name

    message_body = eval(message['Body'])
    if message_body is None:
        print('parse_message: No message body.')
        return False

    job = message_body['job']
    job_id = job['id']
    if job_id is None:
        print('parse_message: No job id.')
        return False

    source_name = job['source']
    if source_name is None:
        print('parse_message: No source name.')
        return False

    tool_name = job['tool']
    if tool_name is None:
        print('parse_message: No tool name.')
        return False

    # successfully parsed message
    return True


def download_source(bucket_name, source_name):
    # get bucket
    s3util.list_buckets()
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        printf(f'Bucket {bucket_name} does not exist.')
        return False

    # download file
    file_name = source_name
    success = s3util.download_file(bucket_name, source_name, file_name)
    if not success:
        printf(f'Failed to download source file: {source_name}.')
        return False

    # successfully uploaded file
    return True


def extract_source_files(source_name):
    process = subprocess.Popen(['tar', '-xvf', source_name],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)

    while True:
        output = process.stdout.readline()
        print(output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output
            for output in process.stdout.readlines():
                print(output.strip())
            break

    # finished extracting source files
    return True


def run_tool(tool_name):
    process = subprocess.Popen([tool_name, 'input/preprocess/*.i', 'jobLog.py', 'log.v'],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)

    while True:
        output = process.stdout.readline()
        print(output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output
            for output in process.stdout.readlines():
                print(output.strip())
            break

    # finished extracting source files
    return True


def main():
    print('\nStarting processJob.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('\nEnv vars:')
    print(f'bucket_name: {bucket_name}')
    print(f'queue_name: {queue_name}')

    message = receive_message(queue_name)
    if message is None:
        print('receive_message failed.  Exit.')
        return

    print('\nMessage:')
    print(message)

    success = parse_message(message)
    if not success:
        print('parse_message failed.  Exit.')
        return

    print('\nBody attributes:')
    print(f'job_id: {job_id}')
    print(f'source_name: {source_name}')
    print(f'tool_name: {tool_name}')

    success = download_source(bucket_name, source_name)
    if not success:
        print('upload_source failed.  Exit.')
        return

    success = extract_source_files(source_name)
    if not success:
        print('extract_source_files failes.  Exit.')
        return

    success = run_tool(tool_name)
    if not success:
        print('run_tool failed.  Exit.')
        return


if __name__ == '__main__':
    main()

