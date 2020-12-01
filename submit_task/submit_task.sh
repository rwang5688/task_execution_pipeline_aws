#!/bin/bash
# set env vars
. $SUBMIT_TASK/env.sh

# submit task based on task_id1_context_user_id.json
# read ./xcalagent contents: fileinfo.json, preprocess.tar.gz, source_code.zip
echo "[CMD] python3 $SUBMIT_TASK/submit_task.py $1"
python3 $SUBMIT_TASK/submit_task.py $1

