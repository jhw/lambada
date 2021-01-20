import json, os

from urllib import request

StackMessage="%s | phase `%s` | status `%s`"

def post_json(url, struct):
    req=request.Request(url, method="POST")
    req.add_header("Content-Type", "application/json")
    data=json.dumps(struct).encode()
    resp=request.urlopen(req, data=data)
    return resp.read()

def parse_message(message):
    return json.loads(message.replace(chr(10), "")[1:-1].replace("'", "\""))

def handle_record(record,
                  template=StackMessage,
                  url=os.environ["WEBHOOK_URL"]):
    message=parse_message(record["Sns"]["Message"])
    print (message)
    text=template % (message["build-id"],
                     message["completed-phase"],
                     message["completed-phase-status"])    
    req={"text": text}
    print (req)
    resp=post_json(url, req)
    print (resp)
    
def handler(event, context):
    for record in event["Records"]:
        handle_record(record)
        
if __name__=="__main__":
    pass
