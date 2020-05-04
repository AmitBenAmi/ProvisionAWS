class HttpSecurityGroup:
    def __init__(self, ec2_client, vpc_id: str):
        self.__client = ec2_client
        self.__name = 'http-security-group'
        self.__vpc_id = vpc_id
    
    def create(self):
        response = self.__client.create_security_group(
            Description='Allows HTTP traffic',
            GroupName=self.__name,
            VpcId=self.__vpc_id
        )

        self.__id = response['GroupId']