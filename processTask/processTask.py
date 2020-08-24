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
    if 'TASK_LIST_SOURCE_DATA_BUCKET' in os.environ:
        bucket_name = os.environ['TASK_LIST_SOURCE_DATA_BUCKET']

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
    global task_id
    global task_tool
    global task_source

    message_body = eval(message['Body'])
    if message_body is None:
        print('parse_message: message body is missing.')
        return False

    task = message_body['task']
    if task is None:
        print('parse_message: task is missing.')
        return False

    task_id = task['task_id']
    if task_id is None:
        print('parse_message: task id is missing.')
        return False

    task_tool = task['task_tool']
    if task_tool is None:
        print('parse_message: task tool is missing.')
        return False

    task_source = task['task_source']
    if task_source is None:
        print('parse_message: task source is missing.')
        return False

    # success
    return True


def download_source_blob(bucket_name, task_source):
    # get bucket
    s3util.list_buckets()
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print(f'download_source_file: Bucket {bucket_name} does not exist.')
        return None

    # download file
    source_blob = task_source
    success = s3util.download_file(bucket_name, task_source, source_blob)
    if not success:
        print(f'download_source_file: Failed to download task source {task_source}.')
        return None

    # success
    return source_blob


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


def extract_source_files(source_blob):
    # command: "$ tar -xvf $(task_source)"
    process = subprocess.Popen(['tar', '-xvf', source_blob],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    read_process_stdout(process)

    # success
    return True


def execute_tool(task_tool, task_id):
    # command: "$ $(task_tool) source/preprocess/*.i taskLog.py $(task_id)"
    prog = './' + task_tool
    process = subprocess.Popen([prog, 'source/preprocess/*.i', 'taskLog.py', task_id],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
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
    print(f'task_id: {task_id}')
    print(f'task_tool: {task_tool}')
    print(f'task_source: {task_source}')

    source_blob = download_source_blob(bucket_name, task_source)
    if source_blob is None:
        print('download_source_blob failed.  Exit.')
        return

    print(f'source_blob: {source_blob}')

    success = extract_source_files(source_blob)
    if not success:
        print('extract_source_files failed.  Exit.')
        return

    success = execute_tool(task_tool, task_id)
    if not success:
        print('execute_tool failed.  Exit.')
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

