#!/usr/bin/env python

import boto3, sys, yaml

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
        builds=get_builds(cb, config)
        latest=builds.pop()
        print ("%i/%i\t%s\t%s" % (1+i,
                                  maxtries,
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
        logging.error(str(error))
    except RuntimeError as error:
        logging.error(str(error))

