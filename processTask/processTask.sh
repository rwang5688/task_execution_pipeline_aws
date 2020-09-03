#!/bin/bash
# set env vars
. ./env.sh

# retrieve task, set task_id, set task_extra_options and download files
echo "[CMD] python3 processTask.py"
python3 processTask.py

# print env vars
#echo "SCAN_TASK_ID: ${SCAN_TASK_ID}"
#echo "SCAN_EXTRA_OPTIONS: ${SCAN_EXTRA_OPTIONS}"
#echo "SCAN_EXTRA_JFE_OPTIONS: ${SCAN_EXTRA_JFE_OPTIONS}"
#echo "SCAN_EXTRA_VARIABLE_OPTION: ${SCAN_EXTRA_VARIABLE_OPTION}"
#echo "SCAN_EXTRA_SKIP_VTABLE_OPTION: ${SCAN_EXTRA_VTABLE_OPTION}"

