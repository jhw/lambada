#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Please enter app name"
    exit
fi

# https://unix.stackexchange.com/questions/312280/split-string-by-delimiter-and-get-n-th-element

appname="$(cut -d'.' -f1 <<<"$1")"

aws cloudformation describe-stacks --stack-name $appname-lambada-ci --query 'Stacks[0].Outputs' --output table
