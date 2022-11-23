#!/bin/bash

TYPE=$1
MODEL=$2
MODEL_NAME=$3
LOCATION=$4

TEST_SELECTION=$TYPE

if [ "$TEST_SELECTION" = "pd" ]; then
    PARAMETERS=$PROCESS_DATA
elif [ "$TEST_SELECTION" = "sl" ]; then
    PARAMETERS=$SELECT_LOCATION
elif [ "$TEST_SELECTION" = "cca" ]; then
    PARAMETERS=$CALCULATE_COSTS_ALL
else
    PARAMETERS=$TYPE
fi

echo "$1 $2 $3 $4"

echo "... Parameters: $PARAMETERS"
 ../app/main.py --parameters="$PARAMETERS"
