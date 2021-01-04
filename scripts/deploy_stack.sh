#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Please enter app name, template"
    exit
fi

if [ $# -eq 0 ]
then
    echo "Please enter app name, template"
    exit
fi

aws cloudformation deploy --stack-name $1 --template-file $2 --parameter-overrides AppName=$1 --capabilities CAPABILITY_NAMED_IAM
