import configparser
import constants
from ecs import ECSClient, Cluster, TaskDefinition, Service
from ec2 import EC2Client, PrivateNetwork, HttpSecurityGroup
from elb import ELBClient, TargetGroup, ApplicationLoadBalancer
from iam import IAMClient, IAMResource, LogsPolicy, TaskExecutionRolePolicy

config = configparser.SafeConfigParser()
config.read('config.ini')

ec2_config = dict(config.items(constants.EC2_CONFIG_SECTION))
ec2_client = EC2Client().client
vpc = PrivateNetwork(ec2_client=ec2_client, cidr=ec2_config['vpc_cidr'], subnet_cidr=ec2_config['subnet_cidr'], multiple_subnets_cidr_template=ec2_config['multiple_subnet_cidr_template'], internet_gateway_cidr=ec2_config['internet_gateway_cidr'])
vpc.create_with_public_subnet(all_availability_zones=True)

elb_config = dict(config.items(constants.ELB_CONFIG_SECTION))
elb_client = ELBClient().client
target_group = TargetGroup(elbv2_client=elb_client, protocol='HTTP', vpc_id=vpc.id, name=elb_config['target_group_name'], port=elb_config['target_group_port'], health_check_path=elb_config['target_group_health_check_path'], health_check_interval=elb_config['target_group_health_check_interval'], health_check_timeout=elb_config['target_group_health_check_timeout'])
target_group.create()

security_group = HttpSecurityGroup(ec2_client=ec2_client, vpc_id=vpc.id, group_name=ec2_config['http_security_group_name'], port=ec2_config['http_security_group_ingress_port'], incoming_cidr=ec2_config['internet_gateway_cidr'])
security_group.create()
vpc_default_security_group = security_group.vpc_default_security_group()

container_config = dict(config.items(constants.CONTAINER_CONFIG_SECTION))
vpc_subnets_ids = list(map(lambda subnet: subnet.id, vpc.subnets))
load_balancer = ApplicationLoadBalancer(elbv2_client=elb_client, target_group=target_group, container_name=container_config['container_name'], container_port=container_config['container_port'], public_subnet_ids=vpc_subnets_ids, security_groups_ids=[security_group.id, vpc_default_security_group], name=elb_config['load_balancer_name'])
load_balancer.create()
load_balancer.create_listener()

iam_config = dict(config.items(constants.IAM_CONFIG_SECTION))
iam_client = IAMClient().client
execution_role = TaskExecutionRolePolicy(iam_client=iam_client, role_name=iam_config['execution_task_role_name'], policy_arn=iam_config['execution_task_policy_arn'])
policy = LogsPolicy(iam_client=iam_client, logs_policy_name=iam_config['logs_policy'])
policy.create()
execution_role.create(extra_policies=[policy])

ecs_config = dict(config.items(constants.ECS_CONFIG_SECTION))
ecs_client = ECSClient().client
cluster = Cluster(ecs_client=ecs_client, cluster_name=ecs_config['cluster_name'])
cluster.create()

cloud_watch_config = dict(config.items(constants.CLOUD_WATCH_CONFIG_SECTION))
task = TaskDefinition(ecs_client=ecs_client, execution_role_arn=execution_role.role_arn, family=ecs_config['task_family_name'])
task.register(container_name=container_config['container_name'], container_image=container_config['container_image'], container_port=container_config['container_port'], container_port_env_variable_name=container_config['container_port_env_variable_name'], task_vcpu=ecs_config['task_vcpu'], task_memory_in_gb=ecs_config['memory_in_gb'], awslogs_group=cloud_watch_config['group_name'], awslogs_stream_prefix=cloud_watch_config['stream_prefix'])

service = Service(ecs_client=ecs_client,cluster_name=cluster.arn, task_definition=task.arn, desired_count=10, load_balancer=load_balancer, vpc=vpc, name=ecs_config['service_name'])
service.create()

task.wait(cluster_arn=cluster.arn, service_name=service.name)