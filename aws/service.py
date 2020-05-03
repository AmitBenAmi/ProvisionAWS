from appLoadBalancer import ApplicationLoadBalancer
import math

class Service:
    def __init__(self, ecs_client, cluster_name: str, task_definition: str, desirec_count: int, load_balancer: ApplicationLoadBalancer, name: str ='web_service'):
        self.__client = ecs_client
        self.__cluster_name = cluster_name
        self.__name = name
        self.__task_definition = task_definition
        self.__desired_count = desirec_count
        self.__load_balancer = load_balancer
    
    def create(self):
        # We use rolling update deployment type, and therefore I want only one task to be created each time (for resources reasons)
        maximum_percentage = math.ceil((self.__desired_count + 1) * 100 / self.__desired_count)

        response = self.__client.create_service(
            cluster=self.__cluster_name,
            serviceName=self.__name,
            taskDefinition=self.__task_definition,
            loadBalancers=[self.__load_balancer.definition()],
            desiredCount=self.__desired_count,
            launchType='FARGATE',
            deploymentConfiguration={
                'maximumPercent': maximum_percentage,
                'minimumHealthyPercent': 100
            },
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [
                        '10.0.0.0'
                    ]
                }
            },
            healthCheckGracePeriodSeconds=10,
            schedulingStrategy='REPLICA',
            deploymentController={
                'type': 'ECS'
            },
            tags=[
                {
                    'key': 'Applicant',
                    'value': 'Amit Ben Ami'
                },
                {
                    'key': 'Position',
                    'value': 'DevOps Engineer'
                }
            ]
        )