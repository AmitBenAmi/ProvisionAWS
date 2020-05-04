import json

class LogsPolicy:
    def __init__(self, iam_client, logs_policy_name: str):
        self.__client = iam_client
        self.__name = logs_policy_name
    
    @property
    def arn(self):
        return self.__arn
    
    def create(self):
        policy_document = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {   
                    "Effect": "Allow",
                    "Resource": [
                        "arn:aws:logs:*:*:*"
                    ],
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                        "logs:DescribeLogStreams"
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

        self.__wait()
    
    def delete(self):
        response = self.__client.delete_policy(
            PolicyArn=self.__arn
        )
    
    def __wait(self):
        try:
            waiter = self.__client.get_waiter('policy_exists')
            waiter.wait(
                PolicyArn=self.__arn
            )
        except botocore.exceptions.WaiterError as e:
            print(f'Error waiting for the policy. Error: {e.message}')