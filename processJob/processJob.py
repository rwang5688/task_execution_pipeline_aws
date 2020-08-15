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
    if 'JOBS_LIST_SOURCE_DATA_BUCKET' in os.environ:
        bucket_name = os.environ['JOBS_LIST_SOURCE_DATA_BUCKET']

    queue_name = ''
    if 'JOBS_LIST_PROCESS_JOB_QUEUE' in os.environ:
        queue_name = os.environ['JOBS_LIST_PROCESS_JOB_QUEUE']

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
    global job_id
    global job_tool
    global job_source

    message_body = eval(message['Body'])
    if message_body is None:
        print('parse_message: message body is missing.')
        return False

    job = message_body['job']
    if job is None:
        print('parse_message: job is missing.')
        return False

    job_id = job['job_id']
    if job_id is None:
        print('parse_message: job id is missing.')
        return False

    job_tool = job['job_tool']
    if job_tool is None:
        print('parse_message: job tool is missing.')
        return False

    job_source = job['job_source']
    if job_source is None:
        print('parse_message: job source is missing.')
        return False

    # success
    return True


def download_source_blob(bucket_name, job_source):
    # get bucket
    s3util.list_buckets()
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        printf(f'download_source_file: Bucket {bucket_name} does not exist.')
        return None

    # download file
    source_blob = job_source
    success = s3util.download_file(bucket_name, job_source, source_blob)
    if not success:
        printf(f'download_source_file: Failed to download job source {job_source}.')
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
    # command: "$ tar -xvf $(job_source)"
    process = subprocess.Popen(['tar', '-xvf', source_blob],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    read_process_stdout(process)

    # success
    return True


def execute_tool(job_tool, job_id):
    # command: "$ $(job_tool) source/preprocess/*.i jobLog.py $(job_id)"
    prog = './' + job_tool
    process = subprocess.Popen([prog, 'source/preprocess/*.i', 'jobLog.py', job_id],
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
    print('\nStarting processJob.py ...')

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

    print('Body.job:')
    print(f'job_id: {job_id}')
    print(f'job_tool: {job_tool}')
    print(f'job_source: {job_source}')

    source_blob = download_source_blob(bucket_name, job_source)
    if source_blob is None:
        print('download_source_blob failed.  Exit.')
        return

    print(f'source_blob: {source_blob}')

    success = extract_source_files(source_blob)
    if not success:
        print('extract_source_files failed.  Exit.')
        return

    success = execute_tool(job_tool, job_id)
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

