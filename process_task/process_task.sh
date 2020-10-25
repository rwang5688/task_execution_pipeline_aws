#!/bin/bash
# set env vars
. ./env.sh

# set PATH for executables
export PATH=$PATH:$PWD/bin

# retrieve task, set task_id, set task_extra_options and download files
echo "[CMD] python3 process_task.py"
python3 process_task.py

