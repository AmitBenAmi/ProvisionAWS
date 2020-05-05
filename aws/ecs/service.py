import botocore
import math

class Service:
    def __init__(
        self, 
        ecs_client, 
        cluster_name: str, 
        task_definition: str, 
        desired_count: int, 
        load_balancer_definition: dict, 
        publish_subnet_ids: list,
        name: str
    ):
        self.__client = ecs_client
        self.__cluster_name = cluster_name
        self.__name = name
        self.__task_definition = task_definition
        self.__desired_count = desired_count
        self.__publish_subnet_ids = publish_subnet_ids
        self.__load_balancer_definition = load_balancer_definition
    
    @property
    def name(self):
        return self.__name
    
    def create(self):
        # We use rolling update deployment type, and therefore I want only one task to be created each time (for resources reasons)
        maximum_percentage = math.ceil((self.__desired_count + 1) * 100 / self.__desired_count)

        response = self.__client.create_service(
            cluster=self.__cluster_name,
            serviceName=self.__name,
            taskDefinition=self.__task_definition,
            loadBalancers=[self.__load_balancer_definition],
            desiredCount=self.__desired_count,
            launchType='FARGATE',
            deploymentConfiguration={
                'maximumPercent': maximum_percentage,
                'minimumHealthyPercent': 100
            },
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': self.__publish_subnet_ids,
                    'assignPublicIp': 'ENABLED'
                }
            },
            healthCheckGracePeriodSeconds=10,
            schedulingStrategy='REPLICA',
            deploymentController={
                'type': 'ECS'
            },
        )

        self.__wait()
    
    def __wait(self):
        try:
            waiter = self.__client.get_waiter('services_stable')
            waiter.wait(
                cluster=self.__cluster_name,
                services=[
                    self.__name
                ]
            )
        except botocore.exceptions.WaiterError as e:
            print(f'Error waiting for the service. Error: {e.message}')