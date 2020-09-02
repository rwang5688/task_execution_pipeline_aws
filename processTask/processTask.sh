#!/bin/bash
# set env vars
. ./env.sh

# retrieve task, set task_id, set task_extra_options and download files
echo "[CMD] processTask.py"
python3 ./processTask.py

