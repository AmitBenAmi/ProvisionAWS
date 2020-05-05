class Cluster:
    def __init__(self, ecs_client, cluster_name: str):
        self.__client = ecs_client
        self.__name = cluster_name

    @property
    def arn(self):
        return self.__arn

    @property
    def name(self):
        return self.__name
    
    def create(self):
        print('Creating the ECS cluster')
        response = self.__client.create_cluster(
            clusterName=self.__name,
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

        self.__arn = response['cluster']['clusterArn']
        print(f'ECS cluster created with name: {self.__name}')
    
    def delete(self):
        response = self.__client.delete_cluster(cluster=self.__arn)