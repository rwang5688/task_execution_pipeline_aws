#!/usr/bin/env python
import os
import logging
import jsonpickle
import boto3
from botocore.exceptions import ClientError
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import s3util
import sqsutil
import json
import jsonutil


logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()


def createJob(event, context):
    client = boto3.client('lambda')
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))
    response = client.get_account_settings()
    return response['AccountUsage']


def main():
    xray_recorder.begin_segment('main_function')
    file = open('event.json', 'rb')
    try:
      ba = bytearray(file.read())
      event = jsonpickle.decode(ba)
      logger.warning('## EVENT')
      logger.warning(jsonpickle.encode(event))
      context = {'requestid' : '1234'}
      result = createJob(event, context)
      print(str(result))
    finally:
      file.close()
    file.close()
    xray_recorder.end_segment()


if __name__ == '__main__':
    main()

