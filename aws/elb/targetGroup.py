class TargetGroup:
    def __init__(
        self, 
        elbv2_client, 
        protocol: str, 
        vpc_id: str, 
        name: str ='web_target_group_http', 
        port: int =80, 
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

    def create(self):
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

        self.__arn = response['TargetGroups']['TargetGroupArn']