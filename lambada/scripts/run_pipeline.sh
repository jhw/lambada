#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Please enter pipeline name"
    exit
fi

# https://unix.stackexchange.com/questions/312280/split-string-by-delimiter-and-get-n-th-element

pipename="$(cut -d'.' -f1 <<<"$1")"

aws codepipeline start-pipeline-execution --name $pipename --output table

