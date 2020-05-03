class Cluster:
    def __init__(self, ecs_client, cluster_name: str):
        self.__client = ecs_client
        self.__cluster_name = cluster_name
    
    def create(self):
        response = self.__client.create_cluster(
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