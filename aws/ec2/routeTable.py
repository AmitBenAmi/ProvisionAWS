class RouteTable:
    def __init__(self, ec2_client, vpc_id: str):
        self.__ec2_client = ec2_client
        self.__vpc_id = vpc_id
    
    def create(self):
        response = self.__ec2_client.create_route_table(VpcId=self.__vpc_id)