import boto3

class ELBClient:
    def __init__(self):
        self.__client = boto3.client('elbv2')
    
    @property
    def client(self):
        return self.__client