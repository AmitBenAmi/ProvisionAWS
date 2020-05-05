from elb import TargetGroup
import botocore

class ApplicationLoadBalancer:
    def __init__(
        self, 
        elbv2_client, 
        target_group: TargetGroup, 
        container_name: str, 
        container_port: int, 
        public_subnet_ids: list,
        security_groups_ids: list,
        name: str
    ):
        self.__client = elbv2_client
        self.__target_group = target_group
        self.__container_name = container_name
        self.__container_port = container_port
        self.__public_subnet_ids = public_subnet_ids
        self.__security_groups_ids = security_groups_ids
        self.__name = name
    
    @property
    def dns(self):
        return self.__dns

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
            SecurityGroups=self.__security_groups_ids,
            Scheme='internet-facing',
            Type='application',
            IpAddressType='ipv4'
        )

        self.__arn = response['LoadBalancers'][0]['LoadBalancerArn']
        self.__dns = response['LoadBalancers'][0]['DNSName']

        self.__wait()
    
    def create_listener(self, certificate_arn: str):
        ssl_policy = None
        certificates = []
        if self.__target_group.protocol == 'HTTPS':
            ssl_policy = 'ELBSecurityPolicy-2016-08'
            certificates.append(
                {
                    'CertificateArn': certificate_arn
                }
            )

        response = self.__client.create_listener(
            LoadBalancerArn=self.__arn,
            Protocol=self.__target_group.protocol,
            Port=self.__target_group.port,
            DefaultActions=[
                {
                    'Type': 'forward',
                    'TargetGroupArn': self.__target_group.arn
                }
            ],
            SslPolicy=ssl_policy,
            Certificates=certificates
        )
    
    def delete(self):
        response = self.__client.delete_load_balancer(
            LoadBalancerArn=self.__arn
        )
    
    def __wait(self):
        try:
            waiter = self.__client.get_waiter('load_balancer_available')
            waiter.wait(
                LoadBalancerArns=[
                    self.__arn
                ]
            )
        except botocore.exceptions.WaiterError as e:
            print(f'Error waiting for the Load Balancer. Error: {e.message}')