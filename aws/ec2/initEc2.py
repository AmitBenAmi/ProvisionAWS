from common import constants
from ec2 import EC2Client, PrivateNetwork, HttpSecurityGroup

class EC2Initializer:
    def __init__(self, config_sections):
        self.__config = dict(config_sections.items(constants.EC2_CONFIG_SECTION))
        self.__client = EC2Client().client
    
    @property
    def vpc_id(self):
        return self.__vpc.id
    
    @property
    def subnets_ids(self):
        return [subnet.id for subnet in self.__vpc.subnets]
    
    @property
    def security_group_ids(self):
        return [self.__security_group.id, self.__vpc.default_security_group()]
    
    def init(self):
        self.__init_vpc()
        self.__init_security_group()
    
    def __init_vpc(self):
        vpc_cidr = self.__config['vpc_cidr']
        subnet_cidr = self.__config['subnet_cidr']
        multiple_subnets_cidr_template = self.__config['multiple_subnet_cidr_template']
        internet_gateway_cidr = self.__config['internet_gateway_cidr']
        self.__vpc = PrivateNetwork(
            ec2_client=self.__client, 
            cidr=vpc_cidr, 
            subnet_cidr=subnet_cidr, 
            multiple_subnets_cidr_template=multiple_subnets_cidr_template, 
            internet_gateway_cidr=internet_gateway_cidr)
            
        self.__vpc.create_with_public_subnet(all_availability_zones=True)
    
    def __init_security_group(self):
        group_name = self.__config['http_security_group_name']
        port = int(self.__config['http_security_group_ingress_port'])
        incoming_cidr = self.__config['internet_gateway_cidr']
        self.__security_group = HttpSecurityGroup(ec2_client=self.__client, vpc_id=self.__vpc.id, group_name=group_name, port=port, incoming_cidr=incoming_cidr)
        self.__security_group.create()