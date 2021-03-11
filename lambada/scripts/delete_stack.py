#!/usr/bin/env python

import boto3, os, sys, yaml

from botocore.exceptions import ClientError, WaiterError

StackNamePattern="%s-lambada-ci"

ArtifactsBucketPattern="%s-lambada-artifacts"

def clean_artifacts(config):
    bucketname=ArtifactsBucketPattern % config["globals"]["app"]
    print ("--- emptying %s ---" % bucketname)
    s3=boto3.client("s3")
    paginator=s3.get_paginator("list_objects_v2")
    pages=paginator.paginate(Bucket=bucketname)
    for struct in pages:
        if "Contents" in struct:
            for obj in struct["Contents"]:
                print ("deleting object %s" % obj["Key"])
                s3.delete_object(Bucket=bucketname,
                                 Key=obj["Key"])

def delete_stack(config):
    stackname=StackNamePattern % config["globals"]["app"]
    print ("--- deleting %s ---" % stackname)
    cf=boto3.client("cloudformation")
    cf.delete_stack(StackName=stackname)
    waiter=cf.get_waiter("stack_delete_complete")
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
        clean_artifacts(config)
        delete_stack(config)
    except ClientError as error:
        print (error)
    except WaiterError as error:
        print (error)                      
    except RuntimeError as error:
        print (error)                      


        
