import botocore

class Subnet:
    def __init__(self, ec2_client, vpc_id: str, cidr: str ='10.0.0.0/24', availability_zone_id: str =None):
        self.__client = ec2_client
        self.__vpc_id = vpc_id
        self.__cidr = cidr
        self.__availability_zone_id = availability_zone_id
    
    @property
    def cidr(self):
        return self.__cidr

    @property
    def id(self):
        return self.__id

    def create(self):
        print('Creating subnet')
        if self.__availability_zone_id:
            response = self.__client.create_subnet(
                AvailabilityZoneId=self.__availability_zone_id,
                CidrBlock=self.__cidr,
                VpcId=self.__vpc_id
            )
        else:
            response = self.__client.create_subnet(
                CidrBlock=self.__cidr,
                VpcId=self.__vpc_id
            )

        self.__id = response['Subnet']['SubnetId']
        print(f'Subnet created with id: {self.__id}')

        self.__wait()
    
    def __wait(self):
        try:
            waiter = self.__client.get_waiter('subnet_available')
            waiter.wait(
                SubnetIds=[
                    self.__id
                ]
            )
        except botocore.exceptions.WaiterError as e:
            print(f'Error waiting for the subnet. Error: {e.message}')