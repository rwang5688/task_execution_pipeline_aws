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
    if 'TASK_LIST_PREPROCESS_DATA_BUCKET' in os.environ:
        bucket_name = os.environ['TASK_LIST_PREPROCESS_DATA_BUCKET']

    queue_name = ''
    if 'TASK_LIST_PROCESS_TASK_QUEUE' in os.environ:
        queue_name = os.environ['TASK_LIST_PROCESS_TASK_QUEUE']

    # success
    return True


def receive_message(queue_name):
    # get queue url
    sqsutil.list_queues()
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'receive_message: {queue_name} does not exist.')
        return None

    # receive message
    message = sqsutil.receive_message(queue_url)
    if message is None:
        print('receive_message: cannot retrieve message.')
        return None
    print('\nReceived message:')
    print(message)

    # successfully received message
    return message


def parse_message(message):
    global task

    message_body = eval(message['Body'])
    if message_body is None:
        print('parse_message: message body is missing.')
        return False

    task = message_body['task']
    if task is None:
        print('parse_message: task is missing.')
        return False

    # success
    return True


def set_env_vars(task):
    os.environ['SCAN_TASK_ID'] = task['task_id']
    os.environ['SCAN_EXTRA_OPTIONS'] = task['task_extra_options']['SCAN_EXTRA_OPTIONS']
    os.environ['SCAN_EXTRA_JFE_OPTIONS'] = task['task_extra_options']['SCAN_EXTRA_JFE_OPTIONS']
    os.environ['SCAN_EXTRA_VARIABLE_OPTION'] = task['task_extra_options']['SCAN_EXTRA_VARIABLE_OPTION']
    os.environ['SCAN_EXTRA_SKIP_VTABLE_OPTION'] = task['task_extra_options']['SCAN_EXTRA_SKIP_VTABLE_OPTION']

    # success
    return True


def download_preprocessed_files(bucket_name, task):
    # get bucket
    s3util.list_buckets()
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print(f'download_preprocssed_files: Bucket {bucket_name} does not exist.')
        return None

    # get folder (task_id)
    task_id = task['task_id']

    # download source fileinfo
    task_source_fileinfo = task['task_source_fileinfo']
    object_key = task_id + "/" + task_source_fileinfo
    success = s3util.download_file(bucket_name, object_key, task_source_fileinfo)
    if not success:
        print(f'download_preprocessed_files: Failed to download task source fileinfo {task_source_fileinfo}.')

    # download preprocessed files
    task_preprocessed_files = task['task_preprocessed_files']
    object_key = task_id + "/" + task_preprocessed_files
    success = s3util.download_file(bucket_name, object_key, task_preprocessed_files)
    if not success:
        print(f'download_preprocessed_file: Failed to download task preprocssed files {task_preprocessed_files}.')
        return None

    # success
    return task_preprocessed_files


def read_process_stdout(process):
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


def execute_tool(task_tool):
    # command: "./$(task_tool)"
    prog = './' + task_tool
    print(f'prog: {prog}')
    process = subprocess.Popen([prog],
        stdout=subprocess.PIPE, universal_newlines=True)
    read_process_stdout(process)

    # success
    return True


def execute_callback(callback, task_id, task_status):
    # command: "./$(task_tool)"
    prog = './' + callback
    process = subprocess.Popen(["python3", prog, task_id, task_status],
        stdout=subprocess.PIPE, universal_newlines=True)
    read_process_stdout(process)

    # success
    return True


def delete_message(queue_name, message):
    # get queue url
    sqsutil.list_queues()
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'delete_message: {queue_name} does not exist.')
        return False

    # delete message
    sqsutil.delete_message(queue_url, message)
    return True


def main():
    print('\nStarting processTask.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print(f'bucket_name: {bucket_name}')
    print(f'queue_name: {queue_name}')

    message = receive_message(queue_name)
    if message is None:
        print('receive_message failed.  Exit.')
        return

    print('Message:')
    print(message)

    success = parse_message(message)
    if not success:
        print('parse_message failed.  Exit.')
        return

    print('Body.task:')
    print(f'task: {task}')

    success = set_env_vars(task)
    if not success:
        print('set_env_vars failed.  Exit.')
        return

    preprocessed_files = download_preprocessed_files(bucket_name, task)
    if preprocessed_files is None:
        print('download_preprocessed_files failed.  Exit.')
        return

    print(f'preprocessed_files: {preprocessed_files}')

    task_tool = task['task_tool']
    success = execute_tool(task_tool)
    if not success:
        print('execute_tool failed.  Exit.')
        return

    callback = 'taskResult.py'
    task_id = task['task_id']
    success = execute_callback(callback, task_id, "Completed")
    if not success:
        print('execute_callback failed.  Exit.')
        return

    success = delete_message(queue_name, message)
    if not success:
        print('delete_message failed.  Exit.')
        return

    # success
    print('\nReceived and deleted message:')
    print(message)


if __name__ == '__main__':
    main()

