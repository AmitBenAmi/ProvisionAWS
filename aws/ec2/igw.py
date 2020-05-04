class InternetGateway:
    def __init__(self, ec2_client, vpc_id: str):
        self.__client = ec2_client
        self.__vpc_id = vpc_id
    
    def create(self):
        response = self.__client.create_internet_gateway()
        self.__id = response['InternetGateway']['InternetGatewayId']
    
    def attach_to_vpc(self):
        response = self.__client.attach_internet_gateway(
            InternetGatewayId=self.__id,
            VpcId=self.__vpc_id
        )