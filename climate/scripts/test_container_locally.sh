#!/bin/bash


source ./aws.keys
echo $AWS_ACCESS_KEY_ID

docker run -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY climate /scripts/default.sh "cca"  &>> test.log
docker container prune -f
