from common import Region
from ec2 import AvailabilityZone, Subnet, RouteTable, InternetGateway
import botocore

class PrivateNetwork:
    def __init__(
        self, 
        ec2_client, 
        cidr: str ='10.0.0.0/16', 
        subnet_cidr: str ='10.0.0.0/24', 
        multiple_subnets_cidr_template: str ='10.0.{}.0/24', 
        internet_gateway_cidr: str = '0.0.0.0/0'
    ):
        self.__client = ec2_client
        self.__cidr = cidr
        self.__subnet_cidr = subnet_cidr
        self.__multiple_subnets_cidr_template = multiple_subnets_cidr_template
        self.__internet_gateway_cidr = internet_gateway_cidr

    @property
    def id(self):
        return self.__id

    @property
    def subnets(self):
        return self.__subnets

    def create(self):
        print('Creating the VPC')
        response = self.__client.create_vpc(CidrBlock=self.__cidr)
        self.__id = response['Vpc']['VpcId']
        print(f'VPC created with id: {self.__id}')

    def subnets_cidr(self):
        return [subnet.cidr for subnet in self.__subnets]

    def __create_subnet(self, cidr: str, availability_zone_id: str = None):
        if availability_zone_id:
            subnet = Subnet(ec2_client=self.__client, vpc_id=self.__id, availability_zone_id=availability_zone_id, cidr=cidr) 
        else:
            subnet = Subnet(ec2_client=self.__client, vpc_id=self.__id, cidr=cidr)

        subnet.create()
        return subnet

    def __create_with_private_subnet(self):
        self.__subnets = [self.__create_subnet(self.__subnet_cidr)]
    
    def __create_private_subnets_on_all_az(self):
        region = Region()
        az = AvailabilityZone(self.__client, region.name)
        self.__subnets = []
        counter = 0

        for zone_id in az.zone_ids():
            subnet = self.__create_subnet(cidr=self.__multiple_subnets_cidr_template.format(counter), availability_zone_id=zone_id)
            counter += 1
            self.__subnets.append(subnet)

    def create_with_public_subnet(self, all_availability_zones: bool):
        self.create()

        if not all_availability_zones:
            self.__create_with_private_subnet()
        else:
            self.__create_private_subnets_on_all_az()

        print('Attaching the Internet Gatewat to the VPC')
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
        route_table.create_public_route(igw.id, cidr=self.__internet_gateway_cidr)
        
        self.__wait()
        
        print('Internet Gatewat attached to the VPC')

    def delete(self):
        response = self.__client.delete_vpc(
            VpcId=self.__id
        )
    
    def __wait(self):
        try:
            waiter = self.__client.get_waiter('vpc_available')
            waiter.wait(
                VpcIds=[
                    self.__id
                ]
            )
        except botocore.exceptions.WaiterError as e:
            print(f'Error waiting for the VPC. Error: {e.message}')
    
    def default_security_group(self):
        response = self.__client.describe_security_groups(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        self.id
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