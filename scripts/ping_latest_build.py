#!/usr/bin/env python

import boto3, os, sys, time, yaml

from botocore.exceptions import ClientError

def ping_build(cb, config,
               wait=3,
               maxtries=100,
                 exitcodes=["SUCCEEDED",
                            "FAILED",
                            "STOPPED"]):
    def get_builds(cb, config):
        resp=cb.list_builds_for_project(projectName=config["globals"]["app"])
        if ("ids" not in resp or
            resp["ids"]==[]):
            raise RuntimeError("no build ids found")
        return cb.batch_get_builds(ids=resp["ids"])["builds"]
    for i in range(maxtries):
        time.sleep(wait)
        builds=sorted(get_builds(cb, config),
                      key=lambda x: x["startTime"])
        latest=builds.pop()
        print ("%i/%i\t%s\t%s\t%s\t%s\t%s" % (1+i,
                                              maxtries,
                                              latest["id"],
                                              latest["startTime"].strftime("%H:%M:%S"),
                                              latest["endTime"].strftime("%H:%M:%S") if "endTime" in latest else "N/A",
                                              latest["currentPhase"],
                                              latest["buildStatus"]))
        if latest["buildStatus"] in exitcodes:
            break
    
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
        ping_build(boto3.client("codebuild"), config)
    except ClientError as error:
        print (error)
    except RuntimeError as error:
        print ("Error: %s" % (str(error)))

