import argparse
import configparser
import requests
from common import constants
from ec2 import EC2Initializer
from elb import ELBInitializer
from iam import IAMInitializer
from ecs import ECSInitializer

config = configparser.ConfigParser()
config.read('config.ini')

def init_infra(desired_servers):
    ec2_initializer = EC2Initializer(config_sections=config)
    ec2_initializer.init()

    iam_initializer = IAMInitializer(config_sections=config)
    iam_initializer.init()

    elb_initializer = ELBInitializer(
        config_sections=config, 
        vpc_id=ec2_initializer.vpc_id, 
        subnets_ids=ec2_initializer.subnets_ids, 
        security_groups_ids=ec2_initializer.security_group_ids,
        certificate_arn=iam_initializer.certificate_arn)
    elb_initializer.init()

    ecs_initializer = ECSInitializer(
        config_sections=config, 
        execution_role_arn=iam_initializer.execution_role_arn, 
        desired_servers=desired_servers,
        load_balancer_definition=elb_initializer.load_balancer_definition,
        publish_subnet_ids=ec2_initializer.subnets_ids)
    ecs_initializer.init()

    cluster_dns = f'{elb_initializer.protocol.lower()}://{elb_initializer.load_balancer_dns}'

    if check_cluster(cluster_dns=cluster_dns):
        print(f'It is now available to go to: {cluster_dns}')
    else:
        print('There is an issue with HTTP Get request to the cluster')

def check_cluster(cluster_dns):
    response = requests.get(url=cluster_dns, verify=False)

    healthcheck_path = dict(config.items(constants.ELB_CONFIG_SECTION))['target_group_health_check_path']
    response_health_check = requests.get(url=f'{cluster_dns}{healthcheck_path}', verify=False)

    return response.status_code == 200 and response_health_check.status_code == 200

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