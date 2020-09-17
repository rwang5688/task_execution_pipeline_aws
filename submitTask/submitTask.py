import os
import json
import uuid
import boto3
from botocore.exceptions import ClientError
import s3util
import sqsutil


def get_env_vars():
    global preprocess_bucket_name
    global result_bucket_name
    global queue_name

    preprocess_bucket_name = ''
    if 'TASK_EXEC_PREPROCESS_DATA_BUCKET' in os.environ:
        preprocess_bucket_name = os.environ['TASK_EXEC_PREPROCESS_DATA_BUCKET']

    result_bucket_name = ''
    if 'TASK_EXEC_RESULT_DATA_BUCKET' in os.environ:
        result_bucket_name = os.environ['TASK_EXEC_RESULT_DATA_BUCKET']

    queue_name = ''
    if 'TASK_EXEC_SUBMIT_TASK_QUEUE' in os.environ:
        queue_name = os.environ['TASK_EXEC_SUBMIT_TASK_QUEUE']

    # success
    return True


def parse_arguments():
    import argparse
    global task_config_file_name

    parser = argparse.ArgumentParser()
    parser.add_argument('task_config_file_name', help='task config file name.')

    args = parser.parse_args()
    task_config_file_name = args.task_config_file_name

    if task_config_file_name is None:
        print('parse_arguments: task_config_file_name is missing.')
        return False

    # success
    return True


def get_json_data(file_name):
    with open(file_name) as f:
        data = json.load(f)
        return data
    return None


def upload_preprocessed_files(preprocess_bucket_name, task_id, task_config):
    # get bucket
    s3util.list_buckets()
    bucket = s3util.get_bucket(preprocess_bucket_name)
    if bucket is None:
        print(f'upload_processed_files: Bucket {preprocess_bucket_name} does not exist.')
        return False

    # debug: list files before
    s3util.list_files(bucket["Name"])

    # upload source fileinfo
    task_source_fileinfo = task_config["task_source_fileinfo"]
    success = s3util.upload_file(task_source_fileinfo, bucket["Name"], task_id + "/" + task_source_fileinfo)
    if not success:
        print(f'upload_preprocessed_files: Failed to upload task source fileinfo {task_source_fileinfo}.')
        return False

    # upload preprocessed files
    task_preprocessed_files = task_config["task_preprocessed_files"]
    success = s3util.upload_file(task_preprocessed_files, bucket["Name"], task_id + "/" + task_preprocessed_files)
    if not success:
        print(f'upload_preprocssed_files: Failed to upload task preprocessed files {task_preprocessed_files}.')
        return False

    # debug: list files after
    s3util.list_files(bucket["Name"])

    # success
    return True


def upload_source_code(result_bucket_name, task_id, task_config):
    # get bucket
    s3util.list_buckets()
    bucket = s3util.get_bucket(result_bucket_name)
    if bucket is None:
        print(f'upload_source_code: Bucket {result_bucket_name} does not exist.')
        return False

    # debug: list files before
    s3util.list_files(bucket["Name"])

    # upload source code
    task_source_code = task_config["task_source_code"]
    success = s3util.upload_file(task_source_code, bucket["Name"], task_id + "/" + task_source_code)
    if not success:
        print(f'upload_source_code: Failed to upload task source code {task_source_code}.')
        return False

    # debug: list files after
    s3util.list_files(bucket["Name"])

    # success
    return True


def send_message(queue_name, task_id, task_config):
    # get queue url
    sqsutil.list_queues()
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'send_message: Queue {queue_name} does not exist.')
        return False

    # assemble message
    message_body = {
        "action": "submit",
        "task": task_config
    }
    message_body["task"]["task_id"] = task_id

    # send message
    message_id = sqsutil.send_message(queue_url, str(message_body))
    print(f'MessageId: {message_id}')
    print(f'MessageBody: {message_body}')

    # debug: receive message
    message = sqsutil.receive_message(queue_url)
    if message is None:
        print(f'send_message: cannot retrieve sent messge.')
        print(f'(When downstream Lambda function is running, missing message is expected.)')
    print('Received message:')
    print(message)

    # success
    return True


def main():
    print('\nStarting submitTask.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print(f'preprocess_bucket_name: {preprocess_bucket_name}')
    print(f'result_bucket_name: {result_bucket_name}')
    print(f'queue_name: {queue_name}')

    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('Args:')
    print(f'task_config_file_name: {task_config_file_name}')

    task_config = get_json_data(task_config_file_name)
    if task_config == None:
        print('get_json_data failed.  Exit.')
        return

    print('Task config:')
    print(task_config)

    task_id = str(uuid.uuid4())

    print(f'task_id: {task_id}')

    success = upload_preprocessed_files(preprocess_bucket_name, task_id, task_config)
    if not success:
        print('upload_preprocessed_files failed.  Exit.')
        return

    success = upload_source_code(result_bucket_name, task_id, task_config)
    if not success:
        print('upload_source_code failed.  Exit.')
        return

    success = send_message(queue_name, task_id, task_config)
    if not success:
        print('send_message failed.  Exit.')
        return


if __name__ == '__main__':
    main()

