import botocore

class TargetGroup:
    def __init__(
        self, 
        elbv2_client, 
        protocol: str, 
        vpc_id: str, 
        name: str, 
        port: int, 
        target_type: str ='ip',
        health_check_path: str ='/',
        health_check_interval: int =30,
        health_check_timeout: int =5
    ):
        self.__client = elbv2_client
        self.__name = name
        self.__protocol = protocol
        self.__port = port
        self.__target_type = target_type
        self.__vpc_id = vpc_id
        self.__health_check_path = health_check_path
        self.__health_check_interval = health_check_interval
        self.__health_check_timeout = health_check_timeout

    @property
    def arn(self):
        return self.__arn

    @property
    def protocol(self):
        return self.__protocol
    
    @property
    def port(self):
        return self.__port

    def create(self):
        print('Creating the Target Group to traffic requests to the ECS cluster')
        response = self.__client.create_target_group(
            Name=self.__name,
            Protocol=self.__protocol,
            Port=self.__port,
            VpcId=self.__vpc_id,
            HealthCheckProtocol=self.__protocol,
            HealthCheckEnabled=True,
            HealthCheckPath=self.__health_check_path,
            HealthCheckIntervalSeconds=self.__health_check_interval,
            HealthCheckTimeoutSeconds=self.__health_check_timeout,
            TargetType=self.__target_type
        )

        self.__arn = response['TargetGroups'][0]['TargetGroupArn']
        print(f'Target Group created with arn: {self.__arn}')

    def delete(self):
        response = self.__client.delete_target_group(
            TargetGroupArn=self.__arn
        )
    
    def wait(self):
        try:
            waiter = self.__client.get_waiter('target_in_service')
            waiter.wait(
                TargetGroupArn=self.__arn
            )
        except botocore.exceptions.WaiterError as e:
            print(f'Error waiting for the Load Balancer. Error: {e.message}')