import json
import botocore

class Role:
    def __init__(self, iam_client, role_name: str):
        self.__iam_client = iam_client
        self.__name = role_name
    
    @property
    def name(self):
        return self.__name
    
    @property
    def arn(self):
        return self.__arn
    
    def create(self):
        assume_role_policy_document = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {   
                    "Effect": "Allow",
                    "Principal": {
                        "Service": [
                            "ecs-tasks.amazonaws.com",
                            "ecs.amazonaws.com"
                        ]
                    },
                    "Action": [
                        "sts:AssumeRole"
                    ]
                }
            ]
        })
        response = self.__iam_client.create_role(
            RoleName=self.__name,
            AssumeRolePolicyDocument=assume_role_policy_document,
            Tags=[
                {
                    'Key': 'Applicant',
                    'Value': 'Amit Ben Ami'
                },
                {
                    'Key': 'Position',
                    'Value': 'DevOps Engineer'
                }
            ]
        )

        self.__arn = response['Role']['Arn']

        self.__wait()

    def delete(self):
        self.__iam_client.delete_role(
            RoleName=self.__name
        )
    
    def __wait(self):
        try:
            waiter = self.__iam_client.get_waiter('role_exists')
            waiter.wait(
                RoleName=self.__name
            )
        except botocore.exceptions.WaiterError as e:
            print(f'Error waiting for the role. Error: {e.message}')