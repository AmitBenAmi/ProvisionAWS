class TaskExecutionRolePolicy:
    def __init__(self, iam_resource, iam_client, role_name: str, policy_arn: str):
        self.__resource = iam_resource
        self.__client = iam_client
        self.__role_name = role_name
        self.__role = self.__resource.Role(self.__role_name)
        self.__policy_arn = policy_arn
    
    def create(self, extra_policies: list):
        response = self.__client.attach_role_policy(
            RoleName=self.__role_name,
            PolicyArn=self.__policy_arn
        )

        for policy in extra_policies:
            response = self.__client.attach_role_policy(
                RoleName=self.__role_name,
                PolicyArn=policy.arn
            )
    
    @property
    def role_arn(self):
        return self.__role.arn
    
    @property
    def role_name(self):
        return self.__role.name