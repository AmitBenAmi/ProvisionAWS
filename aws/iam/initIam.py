from common import constants
from iam import IAMClient, LogsPolicy, TaskExecutionRolePolicy, ServerCertificate

class IAMInitializer:
    def __init__(self, config_sections):
        self.__config = dict(config_sections.items(constants.IAM_CONFIG_SECTION))
        self.__client = IAMClient().client
    
    @property
    def execution_role_arn(self):
        return self.__execution_role.role_arn
    
    def init(self):
        self.__init_policy()
        self.__init_task_execution_role_policy()
        self.__init_server_certificate

    def __init_policy(self):
        logs_policy = self.__config['logs_policy_name']
        self.__policy = LogsPolicy(iam_client=self.__client, logs_policy_name=logs_policy)
        self.__policy.create()
    
    def __init_task_execution_role_policy(self):
        role_name = self.__config['execution_task_role_name']
        policy_arn = self.__config['execution_task_policy_arn']
        self.__execution_role = TaskExecutionRolePolicy(iam_client=self.__client, role_name=role_name, policy_arn=policy_arn)
        self.__execution_role.create(extra_policies=[self.__policy])
    
    def __init_server_certificate(self):
        cert_name = self.__config['server_certificate_name']
        cert_file_location = self.__config['server_certificate_cert_file_location']
        key_file_location = self.__config['server_certificate_key_file_location']
        self.__server_certificate = ServerCertificate(
            self.__client, 
            cert_file_location=cert_file_location, 
            key_file_location=key_file_location, 
            certificate_name=cert_name)
        self.__server_certificate.upload()