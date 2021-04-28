#!/usr/bin/env python

import boto3, os, sys, yaml

from botocore.exceptions import ClientError, WaiterError

StackName="github-src-credential"

"""
https://stackoverflow.com/questions/247770/how-to-retrieve-a-modules-path
"""

def load_path(path):
    import lambada
    return "%s/%s" % (lambada.__path__.__dict__["_path"][0], path)

StackTemplate=open(load_path("assets/pat.yaml")).read()

def deploy_stack(cf, config,
                 stackname=StackName,
                 stackbody=StackTemplate):
    def stack_exists(cf, stackname):
        stacknames=[stack["StackName"]
                    for stack in cf.describe_stacks()["Stacks"]]
        return stackname in stacknames
    def init_params(params):
        return {"PAT": params["repo"]["PAT"]}
    def format_params(params):
        return [{"ParameterKey": k,
                 "ParameterValue": v}
                for k, v in params.items()]
    action="update" if stack_exists(cf, stackname) else "create"
    fn=getattr(cf, "%s_stack" % action)
    params=init_params(config)
    fn(StackName=stackname,
       Parameters=format_params(params),
       TemplateBody=stackbody,
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
    except WaiterError as error:
        print (error)
    except RuntimeError as error:
        print ("Error: %s" % str(error))
