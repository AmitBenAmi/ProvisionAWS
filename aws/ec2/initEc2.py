from common import constants
from ec2 import EC2Client

class EC2Initializer:
    def __init__(self, config):
        self.__config = config
        self.__client = EC2Client().client