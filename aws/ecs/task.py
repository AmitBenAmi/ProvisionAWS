from common import Region

class TaskDefinition:
    def __init__(self, ecs_client, family: str ='web-task-definition', container_name: str ='nodejs'):
        self.__client = ecs_client
        self.__family = family
        self.__container_name = container_name
    
    @property
    def container_name(self):
        return self.__container_name
    
    @property
    def family_and_revision(self):
        return f'{self.__family}:{self.__revision | 1}'
    
    @property
    def arn(self):
        return self.__arn
    
    def register(self):
        region = Region()

        response = self.__client.register_task_definition(
            family=self.__family,
            networkMode='awsvpc',
            containerDefinitions=[
                {
                    'name': self.__container_name,
                    'image': 'amitbenami/server-details:alpine-1.0.0',
                    'portMappings': [
                        {
                            'containerPort': 8080,
                            'protocol': 'tcp'
                        }
                    ],
                    'essential': True,
                    'environment': [
                        {
                            'name': 'WEB_PORT',
                            'value': '8080'
                        }
                    ],
                    'healthCheck': {
                        'command': [ "CMD_SHELL", "wget -qO- http://localhost:8080 || exit 1" ],
                        'startPeriod': 10
                    },
                    'logConfiguration': {
                        'logDriver': 'awslogs',
                        'options': {
                            'awslogs-group': 'awslogs-web',
                            'awslogs-region': region.name,
                            'awslogs-stream-prefix': 'awslogs-web'
                        }
                    }
                },
            ],
            requiresCompatibilities=['FARGATE'],
            cpu='.25 vcpu',
            memory='0.5 GB',
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
    
    def delete(self):
        self.__client.deregister_task_definition(taskDefinition=f'{self.__family}:{self.__revision}')
