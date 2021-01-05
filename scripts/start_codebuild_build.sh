#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Please enter project name"
    exit
fi

aws codebuild start-build --project-name $1

