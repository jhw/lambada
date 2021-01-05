#!/usr/bin/env python

import boto3, os, sys, yaml

from botocore.exceptions import ClientError

def format_kwargs(fn):
    def aws_format(params):
        return [{"ParameterKey": k,
                 "ParameterValue": v}
                for k, v in params.items()]
    def wrapped(kwargs):
        modkwargs={"AppName": kwargs["globals"]["app"],
                   "StagingBucket": kwargs["globals"]["bucket"],
                   "RepoOwner": kwargs["repo"]["owner"],
                   "RepoName": kwargs["repo"]["name"],
                   "RepoBranch": kwargs["repo"]["branch"],
                   "RepoPAT": kwargs["repo"]["PAT"]}
        return fn(aws_format(modkwargs))
    return wrapped

@format_kwargs
def deploy_pipeline(kwargs):
    print (kwargs)

if __name__=="__main__":
    try:
        if len(sys.argv) < 2:
            raise RuntimeError("Please enter config")
        configfile=sys.argv[1]
        if not configfile.endswith("yaml"):
            raise RuntimeError("config must be a yaml file")
        if not os.path.exists(configfile):
            raise RuntimeError("config does not exist")
        config=yaml.safe_load(open(configfile).read())
        deploy_pipeline(config)
    except ClientError as error:
        print (error)
    except RuntimeError as error:
        print ("Error: %s" % str(error))
