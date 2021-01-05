#!/usr/bin/env python

import boto3, os, sys, yaml

from botocore.exceptions import ClientError

PipelineTemplate="templates/pipeline.yaml"

def deploy_stack(cf, config, template=PipelineTemplate):
    def stack_exists(cf, stackname):
        stacknames=[stack["StackName"]
                    for stack in cf.describe_stacks()["Stacks"]]
        return stackname in stacknames
    def init_params(params):
        return {"AppName": params["globals"]["app"],
                "StagingBucket": params["globals"]["bucket"],
                "RepoOwner": params["repo"]["owner"],
                "RepoName": params["repo"]["name"],
                "RepoBranch": params["repo"]["branch"],
                "RepoPAT": params["repo"]["PAT"]}
        return fn(aws_format(modkwargs))
    def format_params(params):
        return [{"ParameterKey": k,
                 "ParameterValue": v}
                for k, v in params.items()]
    stackname=config["globals"]["app"]
    action="update" if stack_exists(cf, stackname) else "create"
    fn=getattr(cf, "%s_stack" % action)
    params=init_params(config)
    body=open(template).read()
    fn(StackName=stackname,
       Parameters=format_params(params),
       TemplateBody=body,
       Capabilities=["CAPABILITY_IAM"])
    waiter=cf.get_waiter("stack_%s_complete" % action)
    waiter.wait(StackName=stackname)

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
        deploy_stack(boto3.client("cloudformation"), config)
    except ClientError as error:
        print (error)
    except RuntimeError as error:
        print ("Error: %s" % str(error))
