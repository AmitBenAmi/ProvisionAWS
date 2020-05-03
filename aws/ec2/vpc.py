from common import Region
from ec2 import AvailabilityZone
from ec2 import Subnet

class PrivateNetwork:
    def __init__(self, ec2_client, cidr: str ='10.0.0.0/16'):
        self.__client = ec2_client
        self.__cidr = cidr

    def create(self):
        response = self.__client.create_vpc(CidrBlock=self.__cidr)
        self.__id = response['Vpc']['VpcId']

    def create_with_subnet(self):
        self.create()

        subnet = Subnet(ec2_client=self.__client, vpc_id=self.__id)
        subnet.create()