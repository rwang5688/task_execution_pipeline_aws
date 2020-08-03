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


# handler
def createJob(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))
    client = boto3.client('lambda')
    response = client.get_account_settings()
    return response['AccountUsage']


# main function for testing and debugging handler
def main():
    xray_recorder.begin_segment('main_function')
    file = open('event.json', 'rb')
    try:
      # read sample event
      ba = bytearray(file.read())
      event = jsonpickle.decode(ba)
      logger.warning('## EVENT')
      logger.warning(jsonpickle.encode(event))
      # create sample context
      context = {'requestid' : '1234'}
      # invoke handler
      result = createJob(event, context)
      # print response
      print('## RESPONSE')
      print(str(result))
    finally:
      file.close()
    file.close()
    xray_recorder.end_segment()


if __name__ == '__main__':
    main()

