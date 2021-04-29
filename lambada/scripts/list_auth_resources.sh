#!/usr/bin/env bash

aws cloudformation describe-stack-resources --stack-name github-src-credential --query "StackResources[].{\"1.Timestamp\":Timestamp,\"2.LogicalId\":LogicalResourceId,\"3.PhysicalId\":PhysicalResourceId,\"4.Type\":ResourceType,\"5.Status\":ResourceStatus}"
