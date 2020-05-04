class RouteTable:
    def __init__(self, ec2_client, vpc_id: str):
        self.__ec2_client = ec2_client
        self.__vpc_id = vpc_id

    @property
    def id(self):
        return self.__id
    
    def create(self):
        response = self.__ec2_client.create_route_table(VpcId=self.__vpc_id)
        self.__id = response['RouteTable']['RouteTableId']
    
    def create_route(self, igw_id: str, cidr: str ='0.0.0.0/0'):
        response = self.__ec2_client.create_route(
            DestinationCidrBlock=cidr,
            GatewayId=igw_id,
            RouteTableId=self.__id
        )