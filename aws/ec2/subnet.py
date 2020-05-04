class Subnet:
    def __init__(self, ec2_client, vpc_id: str, cidr: str ='10.0.0.0/24'):
        self.__client = ec2_client
        self.__vpc_id = vpc_id
        self.__cidr = cidr
    
    @property
    def cidr(self):
        return self.__cidr

    def create(self):
        response = self.__client.create_subnet(
            CidrBlock=self.__cidr,
            VpcId=self.__vpc_id
        )