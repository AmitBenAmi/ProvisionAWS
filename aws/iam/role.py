import json

class Role:
    def __init__(self, iam_client, role_name: str):
        self.__iam_client = iam_client
        self.__name = role_name
    
    @property
    def name(self):
        return self.__name
    
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