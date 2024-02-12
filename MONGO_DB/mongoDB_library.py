import pandas 
from .config import *
import datetime

class mongo_library():

    def __init__(self, coll, name):
        self.collection = coll
        self.name = name
        self.error = open(FILE_ERRORS, "w")

    def getName(self):
        return self.collection
    
    def insert_records(self, df):
        if self.name == "counting":
            if len(df) > 1:
                try:
                    dict = df.to_dict
                    self.collection.insert_many(dict)
                except:
                    self.error.write(
                        f"Connection error: wifiTracker.{self.name} unreachable - {datetime.datetime.now()}\n"
                    )
            else:
                try:
                    dict = df.to_dict
                    self.collection.insert_one(dict)
                except:
                    self.error.write(
                        f"Connection error: wifiTracker.{self.name} unreachable - {datetime.datetime.now()}\n"
                    )
        else:
            self.error.write(
                        f"Wrong collection contacted: wifiTracker.{self.name} - {datetime.datetime.now()}\n"
                    )

    def findBy_class_period(self, room, init_date, final_date):
        try:
            pipeline = [
            {
                "$match" : {
                    "Timestamp" : {"$gte": init_date},
                    "Timestamp" : {"$lte" : final_date},
                    "Room" : room
                }
            }   
            ]
            df_response = pandas.DataFrame(list(self.collection.aggregate(pipeline)))
        except:
            self.error.write(
                        f"Connection error: wifiTracker.{self.name} unreachable - {datetime.datetime.now()}\n"
                    )
        return df_response

    def findBy_period(self, init_date, final_date):
        try:
            pipeline = [
            {
                "$match" : {
                    "Timestamp" : {"$gte": init_date},
                    "Timestamp" : {"$lte" : final_date},
                }
            }   
            ]
            df_response = pandas.DataFrame(list(self.collection.aggregate(pipeline)))
        except:
            self.error.write(
                        f"Connection error: wifiTracker.{self.name} unreachable - {datetime.datetime.now()}\n"
                    )
        return df_response
