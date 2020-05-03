from boto3.session import Session#.Session import client as EcsClient

class Cluster:
    def __init__(self, ecs_client, cluster_name: str):
        self.__ecs = ecs_client
        self.__cluster_name = cluster_name
    
    def create(self):
        response = self.__ecs.create_cluster(
            clusterName=self.__cluster_name,
            tags=[
                {
                    'key': 'Applicant',
                    'value': 'Amit Ben Ami'
                },
                {
                    'key': 'Position',
                    'value': 'DevOps Engineer'
                }
            ],
            settings=[
                {
                    'name': 'containerInsights',
                    'value': 'enabled'
                }
            ],
            capacityProviders=[
                'FARGATE'
            ]
        )