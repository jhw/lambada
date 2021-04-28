#!/usr/bin/env bash

aws cloudformation deploy --stack-name github-src-credential --template-file lambada/assets/auth.yaml --parameter-overrides PAT=$1 --capabilities CAPABILITY_NAMED_IAM
