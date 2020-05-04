class HttpSecurityGroup:
    def __init__(self, ec2_client, vpc_id: str, port: int =80, healthcheck_port: int =8080):
        self.__client = ec2_client
        self.__name = 'http-security-group'
        self.__vpc_id = vpc_id
        self.__port = port
        self.__healthcheck_port = healthcheck_port

    @property
    def id(self):
        return self.__id
    
    def create(self):
        response = self.__client.create_security_group(
            Description='Allows HTTP traffic',
            GroupName=self.__name,
            VpcId=self.__vpc_id
        )

        self.__id = response['GroupId']

        self.__create_ingress()

        vpc_default_group_id = self.__vpc_default_security_group()
        self.__create_egress_for_healthcheck(egress_group_id=vpc_default_group_id)
    
    def __create_ingress(self):
        response = self.__client.authorize_security_group_ingress(
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
    
    def __create_egress_for_healthcheck(self, egress_group_id: str):
        response = self.__client.authorize_security_group_egress(
            GroupId=self.__id,
            IpPermissions=[
                {
                    'FromPort': self.__healthcheck_port,
                    'ToPort': self.__healthcheck_port,
                    'IpProtocol': 'tcp',
                    'UserIdGroupPairs': [
                        {
                            'GroupId': egress_group_id
                        }
                    ]
                }
            ]
        )
    
    def __vpc_default_security_group(self):
        response = self.__client.describe_security_groups(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        self.__vpc_id
                    ]
                },
                {
                    'Name': 'group-name',
                    'Values': [
                        'default'
                    ]
                }
            ]
        )

        return response['SecurityGroups']['GroupId']