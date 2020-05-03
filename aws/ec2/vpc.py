class PrivateNetwork:
    def __init__(self, ec2_client, cidr: str ='10.0.0.0/16'):
        self.__client = ec2_client
        self.__cidr = cidr

    def create(self):
        response = self.__client.create_vpc(CidrBlock=self.__cidr)
