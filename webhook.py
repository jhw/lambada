import json

from urllib import request

def post_json(url, struct):
    req=request.Request(url, method="POST")
    req.add_header("Content-Type", "application/json")
    data=json.dumps(struct).encode()
    resp=request.urlopen(req, data=data)
    return resp.read()

def parse_message(message):
    return json.loads(message.replace(chr(10), "")[1:-1].replace("'", "\""))

def handler(event, context, url="{webhook_url}"):
    for record in event["Records"]:
        message=parse_message(record["Sns"]["Message"])
        print (message)
        struct=dict([("text", str(message))]) # temporarily avoid curly brackets to avoid messing up text substitution
        print (post_json(url, struct))

if __name__=="__main__":
    pass
