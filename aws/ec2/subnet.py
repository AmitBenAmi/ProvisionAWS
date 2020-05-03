class Subnet:
    def __init__(self, ec2_client, availability_zone_id: str, vpc_id: str, cidr: str ='10.0.0.0/24'):
        self.__client = ec2_client
        self.__az_id = availability_zone_id
        self.__vpc_id = vpc_id
        self.__cidr = cidr

    def create(self):
        response = self.__client.create_subnet(
            AvailabilityZoneId=self.__az_id,
            CidrBlock=self.__cidr,
            VpcId=self.__vpc_id
        )