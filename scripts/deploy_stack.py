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
- variables (eg ARTIFACTS) defined in `init_prebuild` and then shared across other phases
- variables defined in `env/variables` don't seem able to resolve environment variables
"""

def init_buildspec(config,
                   version=CodeBuildVersion,
                   runtime=PythonRuntime):
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
    def init_prebuild(config):
        commands=[]
        commands.append("ARTIFACTS=%s-$CODEBUILD_RESOLVED_SOURCE_VERSION.zip" % config["globals"]["app"])
        commands.append("python test.py")
        return {"commands": commands}
    def init_build(config):
        commands=["zip $ARTIFACTS -r %s/** -x */__pycache__/* */test.py" % config["globals"]["app"]]
        return {"commands": commands}
    def init_postbuild(config):
        commands=["aws s3 cp $ARTIFACTS s3://%s/" % config["globals"]["bucket"]]
        return {"commands": commands}
    phases={"install": init_install(config, runtime),
            "pre_build": init_prebuild(config),
            "build": init_build(config),
            "post_build": init_postbuild(config)}
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
    print (yaml.safe_dump(buildspec,
                          default_flow_style=False))
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
