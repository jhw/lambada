import json, logging, urllib

def parse_message(message):
    return json.loads(message.replace(chr(10), "")[1:-1].replace("'", "\""))

def handler(event, context, url="{webhook_url}"):
    for record in event["Records"]:
        message=parse_message(record["Sns"]["Message"])
        print (message)

if __name__=="__main__":
    pass
