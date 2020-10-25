#!/bin/bash

cd ..

# TODO: We need to figure out how to set executable PATH in CICD environment
# set PATH for executables
export PATH=$PATH:$PWD/bin
printenv PATH

export TASK_EXEC_BIN=$PWD/bin
printenv TASK_EXEC_BIN

cd install

