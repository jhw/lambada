#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Please enter app name, max items"
    exit
fi

# https://unix.stackexchange.com/questions/312280/split-string-by-delimiter-and-get-n-th-element

appname="$(cut -d'.' -f1 <<<"$1")"

if [ $# -eq 1 ]
then
    echo "Please enter app name, max items"
    exit
fi

aws cloudformation describe-stack-events --stack-name $appname-lambada-ci --query "StackEvents[].{\"1.Timestamp\":Timestamp,\"2.Id\":LogicalResourceId,\"3.Type\":ResourceType,\"4.Status\":ResourceStatus,\"5.Reason\":ResourceStatusReason}" --max-items $2
