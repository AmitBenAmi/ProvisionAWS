class ApplicationLoadBalancer:
    def __init__(self, elbv2_client, target_group_arn: str, container_name: str, container_port: int, public_subnet_ids: list, name: str ='web_load_balancer'):
        self.__client = elbv2_client
        self.__target_group_arn = target_group_arn
        self.__container_name = container_name
        self.__container_port = container_port
        self.__public_subnet_ids = public_subnet_ids
        self.__name = name

    def definition(self):
        return {
            'targetGroupArn': self.__target_group_arn,
            'containerName': self.__container_name,
            'containerPort': self.__container_port
        }
    
    def create(self):
        response = self.__client.create_load_balancer(
            Name=self.__name,
            Subnets=self.__public_subnet_ids,
            Scheme='internet-facing',
            Tags=[
                {
                    'key': 'Applicant',
                    'value': 'Amit Ben Ami'
                },
                {
                    'key': 'Position',
                    'value': 'DevOps Engineer'
                }
            ],
            Type='application',
            IpAddressType='ipv4'
        )