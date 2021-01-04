#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Please enter project name"
    exit
fi

aws codebuild list-builds-for-project --project-name $1 --output table

