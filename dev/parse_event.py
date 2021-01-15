import json

Event={'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:eu-west-1:119552584133:lamdemo-CodeBuildNotificationTopic-1ERXHALH189QF:923fc8f3-3ff9-4e79-aed9-d8fada1f28b2', 'Sns': {'Type': 'Notification', 'MessageId': '9f79a89e-feeb-519f-b4d3-f0e571ab7c60', 'TopicArn': 'arn:aws:sns:eu-west-1:119552584133:lamdemo-CodeBuildNotificationTopic-1ERXHALH189QF', 'Subject': None, 'Message': '"{\'build-id\': \'arn:aws:codebuild:eu-west-1:119552584133:build/lamdemo:09187446-9be0-4717-8942-b11bc847b772\', \'project-name\': \'lamdemo\', \'completed-phase\': \'FINALIZING\', \'completed-phase-status\': \'SUCCEEDED\'}"\n', 'Timestamp': '2021-01-15T12:39:28.180Z', 'SignatureVersion': '1', 'Signature': 'ttcF9ZEGurA1cNZDO/OcB72kapk8xJIaLfaK0W1SnXeRHA9J4wvmtkk1JwO3fdVSKJbkonY9wDMIdPC3YbuXWyUUgWBxTsfITq8Rnw9v36dvtg/hWT5Ssk//pIYCo41xBcQ16bB+o/Vb9aSRNKWxvgwxTkM5/k+yfyQY4Il5zaXLGb6fJbL41GkcnGW4A5+zjKUG1jycYGFoQA2Wjs5hPuHzfiaeQk5lh5C96wO6OWQ/Wqg3Sf4CuPZrlfzr/iHtUxubpSY+tHxovhpDSvRo8WqyKEffT5Zc/+3UWrIp8oC3sh89PxFVeniTuKo4Q7yXofsZyJS1nVBCwy0Uv9vCdg==', 'SigningCertUrl': 'https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem', 'UnsubscribeUrl': 'https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-1:119552584133:lamdemo-CodeBuildNotificationTopic-1ERXHALH189QF:923fc8f3-3ff9-4e79-aed9-d8fada1f28b2', 'MessageAttributes': {}}}]}

if __name__=="__main__":
    def parse_message(message):
        return json.loads(message.replace("\n", "")[1:-1].replace("'", "\""))
    for record in Event["Records"]:
        print (parse_message(record["Sns"]["Message"]))

