class HttpSecurityGroup:
    def __init__(self, ec2_client, vpc_id: str, port: int =80):
        self.__client = ec2_client
        self.__name = 'http-security-group'
        self.__vpc_id = vpc_id
        self.__port = port
    
    def create(self):
        response = self.__client.create_security_group(
            Description='Allows HTTP traffic',
            GroupName=self.__name,
            VpcId=self.__vpc_id
        )

        self.__id = response['GroupId']
        
        self.__create_ingress()
    
    def __create_ingress(self):
        response = self.__client.authorize_security_group_ingress(
            FromPort=80,
            GroupId=self.__id,
            IpPermissions=[
                {
                    'FromPort': self.__port,
                    'ToPort': self.__port,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': '0.0.0.0/0',
                            'Description': 'HTTP access from all over the world'
                        }
                    ]
                }
            ]
        )