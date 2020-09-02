import os
import subprocess
import boto3
from botocore.exceptions import ClientError
import s3util
import sqsutil


def get_env_vars():
    global log_bucket_name
    global result_bucket_name
    global queue_name

    log_bucket_name = ''
    if 'TASK_LIST_LOG_DATA_BUCKET' in os.environ:
        log_bucket_name = os.environ['TASK_LIST_LOG_DATA_BUCKET']

    result_bucket_name = ''
    if 'TASK_LIST_RESULT_DATA_BUCKET' in os.environ:
        result_bucket_name = os.environ['TASK_LIST_RESULT_DATA_BUCKET']

    queue_name = ''
    if 'TASK_LIST_UPDATE_TASK_QUEUE' in os.environ:
        queue_name = os.environ['TASK_LIST_UPDATE_TASK_QUEUE']

    # success
    return True


def parse_arguments():
    import argparse
    global task_id
    global task_status

    parser = argparse.ArgumentParser()
    parser.add_argument('task_id', help='The id of the task to update.')
    parser.add_argument('task_status', help='The status of the task to update.')

    args = parser.parse_args()
    task_id = args.task_id
    task_status = args.task_status

    if task_id is None:
        print('parse_arguments: task_id is missing.')
        return False

    if task_status is None:
        print('parse_arguments: task_status is missing.')
        return False

    # success
    return True


def upload_file(bucket_name, task_id, file_name):
    # get bucket
    s3util.list_buckets()
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print(f'upload_file: Bucket {bucket_name} does not exist.')
        return False

    # debug: list files before
    s3util.list_files(bucket["Name"])

    # upload file
    object_key = task_id + "/" + file_name
    success = s3util.upload_file(file_name, bucket["Name"], object_key)
    if not success:
        print(f'upload_file: Failed to upload object {object_key}.')
        return False

    # debug: list files after
    s3util.list_files(bucket["Name"])

    # success
    return True


def send_message(queue_name, task_id, task_status):
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
            "task_status": task_status
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
    print('\nStarting taskResult.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print(f'log_bucket_name: {log_bucket_name}')
    print(f'result_bucket_name: {result_bucket_name}')
    print(f'queue_name: {queue_name}')

    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('args:')
    print(f'task_id = {task_id}')
    print(f'task_status = {task_status}')

    success = upload_file(log_bucket_name, task_id, ".scan_log.tar.gz")
    if not success:
        print('upload_file failed: .scan_log.tar.gz.  Exit.')
        return

    success = upload_file(result_bucket_name, task_id, "scan_result.tar.gz")
    if not success:
        print('upload_file failed: scan_result.tar.gz.  Exit.')
        return

    success = send_message(queue_name, task_id, task_status)
    if not success:
        print('send_message failed.  Exit.')
        return


if __name__ == '__main__':
    main()

