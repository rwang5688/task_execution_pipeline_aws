#!/bin/bash
. ../.env
. ../checkenv.sh
python3 ./submitJob.py $1 $2
