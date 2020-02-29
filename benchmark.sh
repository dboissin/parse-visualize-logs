#!/bin/bash

if [ -z "$1" ]
then
    echo "Missing log file argument."
    exit 1
fi

LOG_FILE=$1
CLEAN_LOG_FILE=$(echo $LOG_FILE | sed 's|/|_|g')
RESULT_CSV=out/benchmark_$CLEAN_LOG_FILE.csv

echo 'python,python regex,c,go,rust' > $RESULT_CSV

for i in `seq 0 4`
do
    C_TIME=$(/usr/bin/time -f '%e' python3 analyse-logs-c.py $LOG_FILE 2>&1 1>/dev/null)
    GO_TIME=$(/usr/bin/time -f '%e' python3 analyse-logs-go.py $LOG_FILE 2>&1 1>/dev/null)
    RUST_TIME=$(/usr/bin/time -f '%e' python3 analyse-logs-rust.py $LOG_FILE 2>&1 1>/dev/null)
    PY_TIME=$(/usr/bin/time -f '%e' python3 analyse-logs-fullpy.py $LOG_FILE 2>&1 1>/dev/null)
    PYREGEX_TIME=$(/usr/bin/time -f '%e' python3 analyse-logs-regex.py $LOG_FILE 2>&1 1>/dev/null)
    echo "$PY_TIME,$PYREGEX_TIME,$C_TIME,$GO_TIME,$RUST_TIME" >> $RESULT_CSV
done

