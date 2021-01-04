#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Please enter bucket"
    exit
fi

aws s3 ls s3://$1 --recursive 

