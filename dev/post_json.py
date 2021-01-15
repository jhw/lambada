from urllib import request

import json

def post_json(url, struct):
    req=request.Request(url, method="POST")
    req.add_header("Content-Type", "application/json")
    data=json.dumps(struct).encode()
    resp=request.urlopen(req, data=data)
    return resp.read()

if __name__=="__main__":
    print (post_json("https://hooks.slack.com/services/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", {"text": "Hello World from Python!"}))
