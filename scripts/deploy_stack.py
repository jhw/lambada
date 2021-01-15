#!/usr/bin/env python

import boto3, json, os, sys, yaml

from botocore.exceptions import ClientError

StackTemplate="stack.yaml"

DefaultDeps=yaml.safe_load("""
- name: pip
- name: awscli
""")

CodeBuildVersion, PythonRuntime = "0.2", "3.8"

"""
- using a single phase only to avoid phases continuing to run after failure
- https://stackoverflow.com/questions/46584324/code-build-continues-after-build-fails
- POST_BUILD still runs even if BUILD fails, but if there's nothing in POST_BUILD it doesn't matter
"""

BuildPhase=yaml.safe_load("""
- 'python test.py'
- 'RAW_TAG=$(git describe --tags --abbrev=0)'
- 'echo "RAW_TAG=$RAW_TAG"'
- 'MOD_TAG=$(echo "$RAW_TAG" | sed -e "s/\W/-/g")'
- 'echo "MOD_TAG=$MOD_TAG"'
- 'ARTIFACTS=$APP_NAME-$MOD_TAG.zip'
- 'echo "ARTIFACTS=$ARTIFACTS"'
- 'zip $ARTIFACTS -r $APP_NAME/** -x */__pycache__/* */test.py'
- 'aws s3 cp $ARTIFACTS s3://$BUCKET_NAME/'
""")

Phases={"build": BuildPhase}

WebhookLambda=open("./webhook.py").read()

def init_buildspec(config,
                   version=CodeBuildVersion,                   
                   runtime=PythonRuntime,
                   phases=Phases):
    def init_variables(config):
        return {"APP_NAME": config["globals"]["app"],
                "BUCKET_NAME": config["globals"]["bucket"]}
    def init_install(config, runtime,
                     defaultdeps=DefaultDeps):
        commands=["apt-get update",
                  "apt-get install zip -y"]
        deps=defaultdeps
        if "deps" in config:
            deps+=config["deps"]
        for dep in deps:
            if "repo" in dep:
                host=dep["repo"]["host"]
                if not host.endswith(".com"):
                    host+=".com"
                source="git+https://%s/%s/%s" % (host,
                                                 dep["repo"]["owner"],
                                                 dep["name"])
                if "version" in dep:
                    source+="@%s" % dep["version"]
            else:
                source=dep["name"]
                if "version" in dep:
                    source+="==%s" % dep["version"]
            command="pip3 install --upgrade %s" % source
            commands.append(command)
        return {"runtime-versions": {"python": runtime},                
                "commands": commands}
    def init_phase(phase):
        return {"commands": phase}
    phases_={"install": init_install(config, runtime),
             "build": init_phase(phases["build"])}
    env={"variables": init_variables(config)}
    return {"version": version,
            "phases": phases_,
            "env": env}

def deploy_stack(cf, config,
                 stackfile=StackTemplate,
                 webhook=WebhookLambda):
    def stack_exists(cf, stackname):
        stacknames=[stack["StackName"]
                    for stack in cf.describe_stacks()["Stacks"]]
        return stackname in stacknames
    def init_params(params, buildspec, webhook):
        return {"AppName": params["globals"]["app"],
                "StagingBucket": params["globals"]["bucket"],
                "RepoOwner": params["repo"]["owner"],
                "RepoName": params["repo"]["name"],
                "RepoBranch": params["repo"]["branch"],
                "RepoPAT": params["repo"]["PAT"],
                "CodeBuildBuildSpec": yaml.safe_dump(buildspec),
                "WebhookUrl": params["slack"]["webhook"],
                "WebhookLambda": webhook}
        return fn(aws_format(modkwargs))
    def format_params(params):
        return [{"ParameterKey": k,
                 "ParameterValue": v}
                for k, v in params.items()]
    stackname=config["globals"]["app"]
    action="update" if stack_exists(cf, stackname) else "create"
    fn=getattr(cf, "%s_stack" % action)
    buildspec=init_buildspec(config)
    print ("--- buildspec.yaml")
    print (yaml.safe_dump(buildspec,
                          default_flow_style=False))
    params=init_params(config, buildspec, webhook)    
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
