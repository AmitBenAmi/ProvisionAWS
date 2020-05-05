import botocore

class HttpSecurityGroup:
    def __init__(self, ec2_client, vpc_id: str, group_name: str, port: int =80, incoming_cidr: str = '0.0.0.0/0'):
        self.__client = ec2_client
        self.__name = group_name
        self.__vpc_id = vpc_id
        self.__port = port
        self.__incoming_cidr = incoming_cidr

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

        self.__wait()
    
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
                            'CidrIp': self.__incoming_cidr,
                            'Description': 'HTTP access from all over the world'
                        }
                    ]
                }
            ]
        )
    
    def vpc_default_security_group(self):
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

        return response['SecurityGroups'][0]['GroupId']
    
    def __wait(self):
        try:
            waiter = self.__client.get_waiter('security_group_exists')
            waiter.wait(
                GroupIds=[
                    self.__id
                ]
            )
        except botocore.exceptions.WaiterError as e:
            print(f'Error waiting for the security group. Error: {e.message}')