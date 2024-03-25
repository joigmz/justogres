import pymongo
from pandas import DataFrame

class Mongo:
    def __init__(self, connection_string:str):
        self.client = pymongo.MongoClient(connection_string)
    
    def df(self, db, collection, pipeline) ->DataFrame:
        result = self.client[db][collection].aggregate(
            pipeline=pipeline
        )
        return DataFrame(list(result))
