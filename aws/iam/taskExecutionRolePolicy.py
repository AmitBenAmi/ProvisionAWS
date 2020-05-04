class TaskExecutionRolePolicy:
    def __init__(self, iam_resource, iam_client):
        self.__resource = iam_resource
        self.__client = iam_client
        self.__role_name = 'ecsTaskExecutionRole'
        self.__role = self.__resource.Role(self.__role_name)
        self.__policy_arn = 'arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy'
    
    def create(self):
        response = self.__client.attach_role_policy(
            RoleName=self.__role_name,
            PolicyArn=self.__policy_arn
        )
    
    @property
    def role_arn(self):
        return self.__role.arn
    
    @property
    def role_name(self):
        return self.__role.name