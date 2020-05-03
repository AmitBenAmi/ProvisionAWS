from boto3.session import Session

class Region:
    def __init__(self):
        session = Session()
        self.__name = session.region_name
    
    @property
    def name(self):
        return self.__name