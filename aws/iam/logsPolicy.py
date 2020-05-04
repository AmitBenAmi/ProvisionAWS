import json

class LogsPolicy:
    def __init__(self, iam_client):
        self.__client = iam_client
        self.__name = 'logs-writing-policy'
    
    @property
    def arn(self):
        return self.__arn
    
    def create(self):
        policy_document = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {   
                    "Effect": "Allow",
                    "Resource": "*",
                    "Action": [
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ]
                }
            ]
        })
        response = self.__client.create_policy(
            PolicyName=self.__name,
            PolicyDocument=policy_document,
            Description='Allows accress to create log stream and write events to log stream on CloudWatch'
        )

        self.__arn = response['Policy']['Arn']