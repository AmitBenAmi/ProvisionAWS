class ServerCertificate:
    def __init__(self, iam_client, cert_file_location: str, key_file_location: str, certificate_name: str):
        self.__client = iam_client
        self.__cert_file_location = cert_file_location
        self.__key_file_location = key_file_location
        self.__name = certificate_name

    @property
    def arn(self):
        return self.__arn
    
    def upload(self):
        with open(self.__cert_file_location) as cert:
            cert_content = cert.read()

        with open(self.__key_file_location) as key:
            key_content = key.read()

        response = self.__client.upload_server_certificate(
            ServerCertificateName=self.__name,
            CertificateBody=cert_content,
            PrivateKey=key_content
        )

        self.__arn = response['ServerCertificateMetadata']['Arn']
    
    def delete(self):
        response = self.__client.delete_server_certificate(
            ServerCertificateName=self.__name
        )