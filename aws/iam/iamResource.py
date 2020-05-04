import boto3

class IAMResource:
    def __init__(self):
        self.__resource = boto3.resource('iam')
    
    @property
    def resource(self):
        return self.__resource