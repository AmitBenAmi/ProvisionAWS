class AvailabilityZone:
    def __init__(self, ec2_client, region_name: str):
        self.__client = ec2_client
        self.__region_name = region_name

    def zone_ids(self):
        if not hasattr(self, '__zones'):
            self.__get_all_zones_for_region()
            
        return [zone['ZoneId'] for zone in self.__zones]

    def __get_all_zones_for_region(self):
        response = self.__client.describe_availability_zones(
            Filters=[
                {
                    'Name': 'region-name',
                    'Values': [
                        self.__region_name
                    ]
                }
            ]
        )

        self.__zones = response['AvailabilityZones']