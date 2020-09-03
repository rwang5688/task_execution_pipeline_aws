#!/bin/bash
# set env vars and PATH
. ./env.sh
export PATH=$PATH:$PWD/bin

# retrieve task, set task_id, set task_extra_options and download files
echo "[CMD] python3 processTask.py"
python3 processTask.py

