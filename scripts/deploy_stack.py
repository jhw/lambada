#!/usr/bin/env python

import boto3, json, os, sys, yaml

from botocore.exceptions import ClientError

StackTemplate="stack.yaml"

def init_buildspec(config,
                   version="0.2",
                   runtime="3.8"):
    def init_install(runtime,
                     deps=["pip",
                           "awscli"]):
        commands=["apt-get update",
                  "apt-get install zip -y"]
        for dep in deps:
            command="pip3 install --upgrade %s" % dep
            commands.append(command)
        return {"runtime-versions": {"python": runtime},                
                "commands": commands}
    def artifacts(appname):
        return "%s-$CODEBUILD_RESOLVED_SOURCE_VERSION.zip" % appname
    def init_build(config):        
        commands=["zip %s -r %s/** -x */__pycache__/* */test.py" % (artifacts(config["globals"]["app"]),
                                                                       config["globals"]["app"])]
        return {"commands": commands}
    def init_postbuild(config):
        commands=["aws s3 cp %s s3://%s/" % (artifacts(config["globals"]["app"]),
                                             config["globals"]["bucket"])]
        return {"commands": commands}
    install, build, postbuild = (init_install(runtime),
                                 init_build(config),
                                 init_postbuild(config))
    phases={"install": install,
            "build": build,
            "post_build": postbuild}
    return {"version": version,
            "phases": phases}

def deploy_stack(cf, config,
                 stackfile=StackTemplate):
    def stack_exists(cf, stackname):
        stacknames=[stack["StackName"]
                    for stack in cf.describe_stacks()["Stacks"]]
        return stackname in stacknames
    def init_params(params, buildspec):
        return {"AppName": params["globals"]["app"],
                "StagingBucket": params["globals"]["bucket"],
                "RepoOwner": params["repo"]["owner"],
                "RepoName": params["repo"]["name"],
                "RepoBranch": params["repo"]["branch"],
                "RepoPAT": params["repo"]["PAT"],
                "CodeBuildBuildSpec": yaml.safe_dump(buildspec)}    
        return fn(aws_format(modkwargs))
    def format_params(params):
        return [{"ParameterKey": k,
                 "ParameterValue": v}
                for k, v in params.items()]
    stackname=config["globals"]["app"]
    action="update" if stack_exists(cf, stackname) else "create"
    fn=getattr(cf, "%s_stack" % action)
    buildspec=init_buildspec(config)
    params=init_params(config, buildspec)
    body=open(stackfile).read()
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
