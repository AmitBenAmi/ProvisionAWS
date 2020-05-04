import boto3

class EC2Client:
    def __init__(self):
        self.__client = boto3.client('ec2')
    
    @property
    def client(self):
        return self.__client