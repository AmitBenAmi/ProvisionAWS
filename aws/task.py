class TaskDefinition:
    def __init__(self, ecs_client, family: str ='web_task_definition', container_name: str ='nodejs'):
        self.__client = ecs_client
        self.__family = family
        self.__container_name = container_name
    
    @property
    def container_name(self):
        return self.__container_name
    
    @property
    def family_and_revision(self):
        return f'{self.__family}:{self.__revision | 1}'
    
    def register(self):
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
    
    def delete(self):
        self.__client.deregister_task_definition(taskDefinition=f'{self.__family}:{self.__revision}')
