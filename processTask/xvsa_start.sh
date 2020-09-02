#!/bin/bash

echo "********************************************"
echo "----- XVSA_START.SH VERSION 2020-08-27 -----"
echo "********************************************"
echo "SCAN_TASK_ID: ${SCAN_TASK_ID}"
echo "SCAN_EXTRA_OPTIONS: ${SCAN_EXTRA_OPTIONS}"
echo "SCAN_EXTRA_JFE_OPTIONS: ${SCAN_EXTRA_JFE_OPTIONS}"
echo "SCAN_EXTRA_VARIABLE_OPTION: ${SCAN_EXTRA_VARIABLE_OPTION}"
echo "SCAN_EXTRA_SKIP_VTABLE_OPTION: ${SCAN_EXTRA_VTABLE_OPTION}"

if [ -f preprocess.tar.gz ]; then
    echo "[CMD] tar -xzf preprocess.tar.gz -C ${SCAN_TASK_ID}.preprocess"
    tar -xzf preprocess.tar.gz -C ${SCAN_TASK_ID}.preprocess
fi

echo "[CMD] xvsa_scan ${SCAN_TASK_ID}.preprocess"
xvsa_scan ${SCAN_TASK_ID}.preprocess

echo "[CMD] tar -cizf .scan_log.tar"
tar -cizf .scan_log.tar .scan_log
echo "[CMD] gzip .scan_log.tar"
gzip -i .scan_log.tar

echo "[CMD] cp scan_result.v ${SCAN_TASK_ID}.v"
cp scan_result/scan_result.v scan_result/${SCAN_TASK_ID}.v

echo "[CMD] tar -cizf scan_result.tar"
tar -cizf scan_result.tar scan_result
echo "[CMD] gzip scan_result.tar"
gzip -i scan_result.tar

