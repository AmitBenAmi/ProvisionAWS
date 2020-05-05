import botocore
from common import Region

class TaskDefinition:
    def __init__(self, ecs_client, execution_role_arn: str, family: str):
        self.__client = ecs_client
        self.__execution_role_arn = execution_role_arn
        self.__family = family
    
    @property
    def family_and_revision(self):
        return f'{self.__family}:{self.__revision | 1}'
    
    @property
    def arn(self):
        return self.__arn
    
    def register(self, container_name: str, container_image: str, container_port: int, container_port_env_variable_name: str, task_vcpu: str, task_memory_in_gb: int, awslogs_group: str, awslogs_stream_prefix: str):
        region = Region()

        response = self.__client.register_task_definition(
            family=self.__family,
            executionRoleArn=self.__execution_role_arn,
            networkMode='awsvpc',
            containerDefinitions=[
                {
                    'name': container_name,
                    'image': container_image,
                    'portMappings': [
                        {
                            'containerPort': container_port,
                            'protocol': 'tcp'
                        }
                    ],
                    'essential': True,
                    'environment': [
                        {
                            'name': container_port_env_variable_name,
                            'value': f'{container_port}'
                        }
                    ],
                    'logConfiguration': {
                        'logDriver': 'awslogs',
                        'options': {
                            'awslogs-create-group': 'true',
                            'awslogs-group': awslogs_group,
                            'awslogs-region': region.name,
                            'awslogs-stream-prefix': awslogs_stream_prefix
                        }
                    }
                },
            ],
            requiresCompatibilities=['FARGATE'],
            cpu=f'{task_vcpu} vcpu',
            memory=f'{task_memory_in_gb} GB',
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

        self.__revision = response['taskDefinition']['revision']
        self.__arn = response['taskDefinition']['taskDefinitionArn']
    
    def deregister(self):
        self.__client.deregister_task_definition(taskDefinition=f'{self.__family}:{self.__revision}')
    
    def __list_for_service(self, cluster_arn: str):
        response = self.__client.list_tasks(
            cluster=cluster_arn,
            family=self.__family
        )

        return response['taskArns']

    def wait(self, cluster_arn: str):
        try:
            waiter = self.__client.get_waiter('tasks_running')
            waiter.wait(
                cluster=cluster_arn,
                tasks=self.__list_for_service(cluster_arn=cluster_arn)
            )
        except botocore.exceptions.WaiterError as e:
            print(f'Error waiting for the task definition. Error: {e.message}')