from application_services.BaseApplicationResource import BaseRDBApplicationResource
from database_services.RDBService import RDBService


class IMDBArtistResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    def get_data_resource_info(cls):
        pass

    @classmethod
    def get_by_name_prefix(cls, name_prefix):
        res = RDBService.get_by_prefix("IMDBFixed", "name_basics",
                                      "primaryName", name_prefix)
        return res