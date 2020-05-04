import configparser
from ecs import ECSClient, Cluster, TaskDefinition, Service
from ec2 import EC2Client, PrivateNetwork, HttpSecurityGroup
from elb import ELBClient, TargetGroup, ApplicationLoadBalancer
from iam import IAMClient, IAMResource, Role, LogsPolicy, TaskExecutionRolePolicy

config = configparser.SafeConfigParser()
config.read('config.ini')

ec2_client = EC2Client().client
vpc = PrivateNetwork(ec2_client=ec2_client)
vpc.create_with_public_subnet(all_availability_zones=True)

elb_client = ELBClient().client
target_group = TargetGroup(elbv2_client=elb_client, protocol='HTTP', vpc_id=vpc.id)
target_group.create()

security_group = HttpSecurityGroup(ec2_client=ec2_client, vpc_id=vpc.id)
security_group.create()
vpc_default_security_group = security_group.vpc_default_security_group()

vpc_subnets_ids = list(map(lambda subnet: subnet.id, vpc.subnets))
load_balancer = ApplicationLoadBalancer(elbv2_client=elb_client, target_group=target_group, container_name='nodejs', container_port=8080, public_subnet_ids=vpc_subnets_ids, security_groups_ids=[security_group.id, vpc_default_security_group])
load_balancer.create()
load_balancer.create_listener()

iam_client = IAMClient().client
iam_resource = IAMResource().resource
execution_role = TaskExecutionRolePolicy(iam_resource=iam_resource, iam_client=iam_client)
role = Role(iam_client=iam_client, role_name=execution_role.role_name)
policy = LogsPolicy(iam_client=iam_client)

role.create()
policy.create()
execution_role.create(extra_policies=[policy])

ecs_client = ECSClient().client
cluster = Cluster(ecs_client=ecs_client)
cluster.create()

task = TaskDefinition(ecs_client=ecs_client, execution_role_arn=execution_role.role_arn)
task.register()

service = Service(ecs_client=ecs_client,cluster_name=cluster.arn, task_definition=task.arn, desired_count=10, load_balancer=load_balancer, vpc=vpc)
service.create()