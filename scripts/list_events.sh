#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Please enter app name"
    exit
fi

aws cloudformation describe-stack-events --stack-name $1 --query "StackEvents[].{\"1.Timestamp\":Timestamp,\"2.Id\":LogicalResourceId,\"3.Type\":ResourceType,\"4.Status\":ResourceStatus,\"5.Reason\":ResourceStatusReason}"
