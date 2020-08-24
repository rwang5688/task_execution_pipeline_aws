import os
import subprocess
import boto3
from botocore.exceptions import ClientError
import s3util
import sqsutil


def get_env_vars():
    global bucket_name
    global queue_name

    bucket_name = ''
    if 'TASK_LIST_LOG_DATA_BUCKET' in os.environ:
        bucket_name = os.environ['TASK_LIST_LOG_DATA_BUCKET']

    queue_name = ''
    if 'TASK_LIST_UPDATE_TASK_QUEUE' in os.environ:
        queue_name = os.environ['TASK_LIST_UPDATE_TASK_QUEUE']

    # success
    return True


def parse_arguments():
    import argparse
    global task_id
    global task_status
    global task_logfile

    parser = argparse.ArgumentParser()
    parser.add_argument('task_id', help='The id of the task to update.')
    parser.add_argument('task_status', help='The status of the task to update.')
    parser.add_argument('task_logfile', help='The logfile of the task to update.')

    args = parser.parse_args()
    task_id = args.task_id
    task_status = args.task_status
    task_logfile = args.task_logfile

    if task_id is None:
        print('parse_arguments: task_id is missing.')
        return False

    if task_status is None:
        print('parse_arguments: task_status is missing.')
        return False

    if task_logfile is None:
        print('parse_arguments: task_logfile is missing.')
        return False

    # success
    return True


def upload_logfile(bucket_name, task_logfile):
    # get bucket
    s3util.list_buckets()
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print(f'upload_logfile: Bucket {bucket_name} does not exist.')
        return False

    # upload file
    s3util.list_files(bucket["Name"])
    success = s3util.upload_file(task_logfile, bucket["Name"])
    if not success:
        print(f'upload_logfile: Failed to upload log file {task_logfile}.')
        return False
    s3util.list_files(bucket["Name"])

    # success
    return True


def send_message(queue_name, task_id, task_status, task_logfile):
    # get queue url
    sqsutil.list_queues()
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'send_message: Queue {queue_name} does not exist.')
        return False

    # send message
    message_body = {
        "action": "update",
        "task": {
            "task_id": task_id,
            "task_status": task_status,
            "task_logfile": task_logfile
        }
    }
    message_id = sqsutil.send_message(queue_url, str(message_body))
    print(f'MessageId: {message_id}')
    print(f'MessageBody: {message_body}')

    # receive message
    message = sqsutil.receive_message(queue_url)
    if message is None:
        print(f'send_message: cannot retrieve sent messge.')
        print(f'(When downstream Lambda function is running, missing message is expected.)')
    print('Received message:')
    print(message)

    # success
    return True


def main():
    print('\nStarting taskLog.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print(f'bucket_name: {bucket_name}')
    print(f'queue_name: {queue_name}')

    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('args:')
    print(f'task_id = {task_id}')
    print(f'task_status = {task_status}')
    print(f'task_logfile = {task_logfile}')

    success = upload_logfile(bucket_name, task_logfile)
    if not success:
        print('upload_logfile failed.  Exit.')
        return

    success = send_message(queue_name, task_id, task_status, task_logfile)
    if not success:
        print('send_message failed.  Exit.')
        return


if __name__ == '__main__':
    main()

