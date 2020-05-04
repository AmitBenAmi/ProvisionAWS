from elb import TargetGroup

class ApplicationLoadBalancer:
    def __init__(
        self, 
        elbv2_client, 
        target_group: TargetGroup, 
        container_name: str, 
        container_port: int, 
        public_subnet_ids: list,
        security_groups: list,
        name: str ='web-load-balancer'
    ):
        self.__client = elbv2_client
        self.__target_group = target_group
        self.__container_name = container_name
        self.__container_port = container_port
        self.__public_subnet_ids = public_subnet_ids
        self.__security_groups = security_groups
        self.__name = name

    def definition(self):
        return {
            'targetGroupArn': self.__target_group.arn,
            'containerName': self.__container_name,
            'containerPort': self.__container_port
        }
    
    def create(self):
        response = self.__client.create_load_balancer(
            Name=self.__name,
            Subnets=self.__public_subnet_ids,
            SecurityGroups=self.__security_groups,
            Scheme='internet-facing',
            Tags=[
                {
                    'Key': 'Applicant',
                    'Value': 'Amit Ben Ami'
                },
                {
                    'Key': 'Position',
                    'Value': 'DevOps Engineer'
                }
            ],
            Type='application',
            IpAddressType='ipv4'
        )

        self.__arn = response['LoadBalancers'][0]['LoadBalancerArn']
    
    def create_listener(self):
        response = self.__client.create_listener(
            LoadBalancerArn=self.__arn,
            Protocol=self.__target_group.protocol,
            Port=self.__target_group.port,
            DefaultActions=[
                {
                    'Type': 'forward',
                    'TargetGroupArn': self.__target_group.arn
                }
            ]
        )