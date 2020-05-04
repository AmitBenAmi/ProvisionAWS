class Cluster:
    def __init__(self, ecs_client, cluster_name: str ='web-cluster'):
        self.__client = ecs_client
        self.__name = cluster_name

    @property
    def arn(self):
        return self.__arn

    @property
    def name(self):
        return self.__name
    
    def create(self):
        response = self.__client.create_cluster(
            clusterName=self.__name,
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

        self.__arn = response['cluster']['clusterArn']
    
    def delete(self):
        response = self.__client.delete_cluster(cluster=self.__name)