import boto3

class ECSClient:
    def __init__(self):
        self.__client = boto3.client('ecs')
    
    @property
    def client(self):
        return self.__client