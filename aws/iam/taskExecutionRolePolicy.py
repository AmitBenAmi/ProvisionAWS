from iam import Role

class TaskExecutionRolePolicy:
    def __init__(self, iam_client, role_name: str, policy_arn: str):
        self.__client = iam_client,
        self.__role_name = role_name,
        self.__policy_arn = policy_arn
        self.__role = Role(iam_client=iam_client, role_name=role_name)
    
    @property
    def role_arn(self):
        return self.__role.arn
    
    @property
    def role_name(self):
        return self.__role.name

    def create(self, extra_policies: list):
        self.__role.create()

        response = self.__client.attach_role_policy(
            RoleName=self.__role_name,
            PolicyArn=self.__policy_arn
        )

        for policy in extra_policies:
            response = self.__client.attach_role_policy(
                RoleName=self.__role_name,
                PolicyArn=policy.arn
            )
    
    def delete(self):
        self.__role.delete()