#!/usr/bin/env python
import os
import subprocess
import boto3
from botocore.exceptions import ClientError
import s3util
import sqsutil


def parse_arguments():
    import argparse
    global log_name

    parser = argparse.ArgumentParser()
    parser.add_argument('log_name', help='The name of the log file to upload')

    args = parser.parse_args()
    log_name = args.log_name

    print('\nargs:')
    print(f'log_name = {log_name}')

    if log_name is None:
        print('log_name is None.')
        return False

    # successfully parsed all arguments
    return True


def main():
    print('\nStarting jobLog.py ...')

    success = parse_arguments()
    if not success:
        print('parse_artuments failed.  Exit.')
        return

if __name__ == '__main__':
    main()

