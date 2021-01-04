#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Please enter app name"
    exit
fi

aws cloudformation describe-stacks --stack-name $1 --query 'Stacks[0].Outputs' --output table
