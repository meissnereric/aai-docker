#!/bin/bash

TAG=${1:aai-default}
REPO=${2:aai-docker-repo}
REGION=${3:eu-west-1}
ACCOUNT=${4:288687564189}


aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT.dkr.ecr.$REGION.amazonaws.com/$REPO

docker build -t $TAG .

docker tag $TAG $ACCOUNT.dkr.ecr.$REGION.amazonaws.com/$REPO:$TAG

 docker push $ACCOUNT.dkr.ecr.$REGION.amazonaws.com/$REPO:$TAG