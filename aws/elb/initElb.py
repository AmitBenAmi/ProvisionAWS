from common import constants
from elb import ELBClient, TargetGroup, ApplicationLoadBalancer

class ELBInitializer:
    def __init__(self, config_sections, vpc_id: str, subnets_ids: list, security_groups_ids: list):
        self.__config = dict(config_sections.items(constants.ELB_CONFIG_SECTION))
        self.__container_config = dict(config_sections.items(constants.CONTAINER_CONFIG_SECTION))
        self.__client = ELBClient().client
        self.__vpc_id = vpc_id
        self.__subnets_ids = subnets_ids
        self.__security_groups_ids = security_groups_ids
    
    @property
    def load_balancer_definition(self):
        return self.__load_balancer.definition()
    
    @property
    def load_balancer_dns(self):
        return self.__load_balancer.dns
    
    @property
    def protocol(self):
        return self.__protocol
    
    def init(self):
        self.__init_target_group()
        self.__init_load_balancer()
        
    def __init_target_group(self):
        self.__protocol = self.__config['target_group_protocol']
        name = self.__config['target_group_name']
        port = int(self.__config['target_group_port'])
        health_check_path = self.__config['target_group_health_check_path']
        health_check_interval = int(self.__config['target_group_health_check_interval'])
        health_check_timeout = int(self.__config['target_group_health_check_timeout'])
        self.__target_group = TargetGroup(
            elbv2_client=self.__client, 
            protocol=self.__protocol, 
            vpc_id=self.__vpc_id, 
            name=name, 
            port=port, 
            health_check_path=health_check_path, 
            health_check_interval=health_check_interval, 
            health_check_timeout=health_check_timeout)
        self.__target_group.create()
    
    def __init_load_balancer(self):
        container_name = self.__container_config['container_name']
        container_port = int(self.__container_config['container_port'])
        name = self.__config['load_balancer_name']
        self.__load_balancer = ApplicationLoadBalancer(
            elbv2_client=self.__client, 
            target_group=self.__target_group, 
            container_name=container_name, 
            container_port=container_port, 
            public_subnet_ids=self.__subnets_ids, 
            security_groups_ids=self.__security_groups_ids, 
            name=name)
            
        self.__load_balancer.create()
        self.__load_balancer.create_listener()