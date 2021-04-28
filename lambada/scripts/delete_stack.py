#!/usr/bin/env python

import boto3, os, sys, yaml

from botocore.exceptions import ClientError, WaiterError

StackNamePattern="%s-lambada-ci"

ArtifactsBucketPattern="%s-lambada-artifacts"

def assert_bucket(fn):
    def wrapped(s3, config):
        bucketname=ArtifactsBucketPattern % config["globals"]["app"]
        resp=s3.list_buckets()
        if "Buckets" not in resp:
            return
        bucketnames=[bucket["Name"]
                     for bucket in resp["Buckets"]]
        if bucketname in bucketnames:
            fn(s3, config)
    return wrapped

@assert_bucket
def clean_artifacts(s3, config):
    bucketname=ArtifactsBucketPattern % config["globals"]["app"]
    print ("--- emptying %s ---" % bucketname)
    paginator=s3.get_paginator("list_objects_v2")
    pages=paginator.paginate(Bucket=bucketname)
    for struct in pages:
        if "Contents" in struct:
            for obj in struct["Contents"]:
                print ("deleting object %s" % obj["Key"])
                s3.delete_object(Bucket=bucketname,
                                 Key=obj["Key"])

def delete_stack(cf, config):
    stackname=StackNamePattern % config["globals"]["app"]
    print ("--- deleting %s ---" % stackname)
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
        clean_artifacts(boto3.client("s3"), config)
        delete_stack(boto3.client("cloudformation"), config)
    except ClientError as error:
        print (error)
    except WaiterError as error:
        print (error)                      
    except RuntimeError as error:
        print (error)                      


        
