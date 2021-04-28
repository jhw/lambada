#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Please enter app name"
    exit
fi

# https://unix.stackexchange.com/questions/312280/split-string-by-delimiter-and-get-n-th-element

appname="$(cut -d'.' -f1 <<<"$1")"

aws cloudformation describe-stack-resources --stack-name $appname-lambada-ci --query "StackResources[].{\"1.Timestamp\":Timestamp,\"2.LogicalId\":LogicalResourceId,\"3.PhysicalId\":PhysicalResourceId,\"4.Type\":ResourceType,\"5.Status\":ResourceStatus}"
