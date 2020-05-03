class TaskDefinition:
    def __init__(self, ecs_client):
        self.__client = ecs_client
    
    def register(self):
        response = self.__client.register_task_definition(
            family='web',
            networkMode='awsvpc',
            containerDefinitions=[
                {
                    'name': 'nodejs',
                    'image': 'amitbenami/server-details:alpine-1.0.0',
                    'command': [
                        'sleep',
                        '360',
                    ],
                    'cpu': 10,
                    'memory': 10,
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
                            'value': 8080
                        }
                    ],
                    'healthCheck': {
                        'command': [ "CMD_SHELL", "wget -qO- http://localhost:8080 || exit 1" ],
                        'startPeriod': 10
                    },
                    'requiresCompatibilities': 'FARGATE',
                    'tags': [
                        {
                            'key': 'Applicant',
                            'value': 'Amit Ben Ami'
                        },
                        {
                            'key': 'Position',
                            'value': 'DevOps Engineer'
                        }
                    ]
                },
            ]
        )
