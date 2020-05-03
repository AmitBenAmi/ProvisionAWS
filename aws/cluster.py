import boto3

class Cluster:
    def __init__(self, ecs_client: boto3.session.Session.client, cluster_name: str):
        self.ecs = ecs_client
        self.cluster_name = cluster_name
    
    def create(self):
        response = self.ecs.create_cluster(
            clusterName=self.cluster_name,
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