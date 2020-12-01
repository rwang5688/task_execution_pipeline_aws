#!/bin/bash

cd ../submit_task

# TODO: We need to figure out how to set executable PATH in CICD environment
# set PATH for executables
export PATH=$PATH:$PWD
printenv PATH

export SUBMIT_TASK=$PWD
printenv SUBMIT_TASK

cd ../install

