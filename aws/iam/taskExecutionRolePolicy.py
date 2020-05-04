class TaskExecutionRolePolicy:
    def __init__(self, iam_resource):
        self.__resource = iam_resource
        self.__role = self.__resource.Role('ecsTaskExecutionRole')
        self.__policy_arn = 'arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy'
    
    def create(self):
        self.__role.attach_policy(PolicyArn=self.__policy_arn)
    
    @property
    def role_arn(self):
        return self.__role.arn