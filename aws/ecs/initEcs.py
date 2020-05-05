from common import constants
from ecs import ECSClient, Cluster, Service, TaskDefinition

class ECSInitializer:
    def __init__(self, config_sections, execution_role_arn: str, desired_servers: int, load_balancer_definition: dict, publish_subnet_ids: list):
        self.__config = dict(config_sections.items(constants.ECS_CONFIG_SECTION))
        self.__cloud_watch_config = dict(config_sections.items(constants.CLOUD_WATCH_CONFIG_SECTION))
        self.__container_config = dict(config_sections.items(constants.CONTAINER_CONFIG_SECTION))
        self.__client = ECSClient().client
        self.__execution_role_arn = execution_role_arn
        self.__desired_servers = desired_servers
        self.__load_balancer_definition = load_balancer_definition
        self.__publish_subnet_ids = publish_subnet_ids
    
    def init(self):
        self.__init_cluster()
        self.__init_task()
        self.__init_service()
    
    def __init_cluster(self):
        cluster_name = self.__config['cluster_name']
        self.__cluster = Cluster(ecs_client=self.__client, cluster_name=cluster_name)
        self.__cluster.create()

    def __init_service(self):
        name = self.__config['service_name']
        self.__service = Service(
            ecs_client=self.__client, 
            cluster_name=self.__cluster.arn, 
            task_definition=self.__task.arn, 
            desired_count=self.__desired_servers, 
            load_balancer_definition=self.__load_balancer_definition, 
            publish_subnet_ids=self.__publish_subnet_ids, 
            name=name)
        self.__service.create()
    
    def __init_task(self):
        family_name = self.__config['task_family_name']
        self.__task = TaskDefinition(ecs_client=self.__client, execution_role_arn=self.__execution_role_arn, family=family_name)

        container_name = self.__container_config['container_name']
        container_image = self.__container_config['container_image']
        container_port = int(self.__container_config['container_port'])
        container_port_env_variable_name = self.__container_config['container_port_env_variable_name']
        task_vcpu = self.__config['task_vcpu']
        task_memory_in_gb = self.__config['memory_in_gb']
        awslogs_group = self.__cloud_watch_config['group_name']
        awslogs_stream_prefix = self.__cloud_watch_config['stream_prefix']
        self.__task.register(
            container_name=container_name, 
            container_image=container_image, 
            container_port=container_port, 
            container_port_env_variable_name=container_port_env_variable_name, 
            task_vcpu=task_vcpu, 
            task_memory_in_gb=task_memory_in_gb,
            awslogs_group=awslogs_group, 
            awslogs_stream_prefix=awslogs_stream_prefix)