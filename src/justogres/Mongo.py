import pymongo
from pymongo.command_cursor import CommandCursor
from pandas import DataFrame

class Mongo:
    def __init__(self, connection_string:str, db, collection, pipeline):
        self.connection_string = connection_string
        self.db = db
        self.collection = collection
        self.pipeline = pipeline
    
    def cursor(self)-> CommandCursor:
        connection = pymongo.MongoClient(self.connection_string)

        result = connection[self.db][self.collection].aggregate(
            pipeline=self.pipeline
        )
        return result
    
    def df(self) ->DataFrame:
        return DataFrame(list(self.cursor()))
