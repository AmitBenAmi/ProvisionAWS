from common import Region
from ec2 import AvailabilityZone
from ec2 import Subnet
from ec2 import RouteTable
from ec2 import InternetGateway

class PrivateNetwork:
    def __init__(self, ec2_client, cidr: str ='10.0.0.0/16'):
        self.__client = ec2_client
        self.__cidr = cidr

    def create(self):
        response = self.__client.create_vpc(CidrBlock=self.__cidr)
        self.__id = response['Vpc']['VpcId']

    def subnet_cidr(self):
        return self.__subnet.cidr

    def create_with_private_subnet(self):
        self.create()

        subnet = Subnet(ec2_client=self.__client, vpc_id=self.__id)
        subnet.create()

        self.__subnet = subnet

    def create_with_public_subnet(self):
        self.create_with_private_subnet()

        igw = InternetGateway(ec2_client=self.__client, vpc_id=self.__id)
        igw.create()
        igw.attach_to_vpc()

        main_route_tables = self.__client.describe_route_tables(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        self.__id
                    ]
                },
                {
                    'Name': 'association.main',
                    'Values': [
                        'true'
                    ]
                }
            ]
        )['RouteTables'][0]

        main_route_table_id = main_route_tables['RouteTableId']
        route_table = RouteTable(ec2_client=self.__client, vpc_id=self.__id, id=main_route_table_id)
        route_table.create_route(igw.id)
