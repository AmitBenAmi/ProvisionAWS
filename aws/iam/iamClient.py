import boto3

class IAMClient:
    def __init__(self):
        self.__client = boto3.client('iam')
    
    @property
    def client(self):
        return self.__client