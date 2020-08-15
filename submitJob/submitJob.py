import os
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
    if 'JOBS_LIST_SUBMIT_JOB_QUEUE' in os.environ:
        queue_name = os.environ['JOBS_LIST_SUBMIT_JOB_QUEUE']

    # success
    return True


def parse_arguments():
    import argparse
    global job_tool
    global job_source

    parser = argparse.ArgumentParser()
    parser.add_argument('job_tool', help='The name of the tool to run.')
    parser.add_argument('job_source', help='The name of the source package to run.')

    args = parser.parse_args()
    job_tool = args.job_tool
    job_source = args.job_source

    if job_tool is None:
        print('parse_arguments: job_tool is missing.')
        return False

    if job_source is None:
        print('parse_arguments: job_source is missing.')
        return False

    # success
    return True


def upload_source(bucket_name, job_source):
    # get bucket
    s3util.list_buckets()
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        printf(f'upload_source: Bucket {bucket_name} does not exist.')
        return False

    # upload file
    s3util.list_files(bucket["Name"])
    success = s3util.upload_file(job_source, bucket["Name"])
    if not success:
        printf(f'upload_source: Failed to upload source file {job_source}.')
        return False
    s3util.list_files(bucket["Name"])

    # success
    return True


def send_message(queue_name, job_tool, job_source):
    # get queue url
    sqsutil.list_queues()
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'send_message: Queue {queue_name} does not exist.')
        return False

    # send message
    message_body = {
        "action": "submit",
        "job": {
            "job_tool": job_tool,
            "job_source": job_source
        }
    }
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
    print('\nStarting submitJob.py ...')

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

    print('Args:')
    print(f'job_tool = {job_tool}')
    print(f'job_source = {job_source}')

    success = upload_source(bucket_name, job_source)
    if not success:
        print('upload_source failed.  Exit.')
        return

    success = send_message(queue_name, job_tool, job_source)
    if not success:
        print('send_message failed.  Exit.')
        return


if __name__ == '__main__':
    main()

