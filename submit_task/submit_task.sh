#!/bin/bash
# set env vars
. $TASK_EXEC_BIN/env.sh

# submit task based on task_id1_context_user_id.json
# read ./xcalagent contents: fileinfo.json, preprocess.tar.gz, source_code.zip
echo "[CMD] python3 $TASK_EXEC_BIN/submit_task.py $1"
python3 $TASK_EXEC_BIN/submit_task.py $1

