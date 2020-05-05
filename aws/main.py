import argparse
import configparser
from ec2 import EC2Initializer
from elb import ELBInitializer
from iam import IAMInitializer
from ecs import ECSInitializer

config = configparser.ConfigParser()
config.read('config.ini')

def init_infra(desired_servers):
    ec2_initializer = EC2Initializer(config_sections=config)
    ec2_initializer.init()

    elb_initializer = ELBInitializer(
        config_sections=config, 
        vpc_id=ec2_initializer.vpc_id, 
        subnets_ids=ec2_initializer.subnets_ids, 
        security_groups_ids=ec2_initializer.security_group_ids)
    elb_initializer.init()

    iam_initializer = IAMInitializer(config_sections=config)
    iam_initializer.init()

    ecs_initializer = ECSInitializer(
        config_sections=config, 
        execution_role_arn=iam_initializer.execution_role_arn, 
        desired_servers=desired_servers,
        load_balancer_definition=elb_initializer.load_balancer_definition,
        publish_subnet_ids=ec2_initializer.subnets_ids)
    ecs_initializer.init()

def create_args():
    parser = argparse.ArgumentParser(description='Provision AWS web servers')
    parser.add_argument('--servers', dest='desired_servers', action='store', nargs=1,
                        help='Set desired servers to provision', default=[1])

    return parser.parse_args()

args = create_args()
desired_servers = int(args.desired_servers[0])
if desired_servers == 0:
    print('Cannot provision 0 servers. Please provide positive number of servers')
else:
    print(f'Going to provision {desired_servers} servers')
    init_infra(desired_servers=desired_servers)