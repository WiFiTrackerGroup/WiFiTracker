import pandas
from config import *
from datetime import datetime
import time
import os


class mongo_library:

    def __init__(self, coll, name):
        self.collection = coll
        self.name = name
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, FILE_ERRORS)
        self.error = open(path, "w")

    def getName(self):
        return self.collection

    def insert_records(self, df):
        if self.name == COUNTNAME:
            if len(df) > 1:
                try:
                    dict = df.T.to_dict().values()
                    self.collection.insert_many(dict)
                except:
                    self.error.write(
                        f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
                    )
            else:
                try:
                    dict = df.to_dict()
                    self.collection.insert_one(dict)
                except:
                    self.error.write(
                        f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
                    )
        elif self.name == TRACKNAME:
            if len(df) > 1:
                try:
                    destination = []
                    for index, row in df.iterrows():
                        for room, people in row.items():
                            if people != 0:
                                destination.append((room, people))
                        dict = {
                            "From": index,
                            "To": destination,
                            "Timestamp": time.time(),
                        }
                        self.collection.insert_one(dict)
                except:
                    self.error.write(
                        f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
                    )
        else:
            self.error.write(
                f"Wrong collection contacted: wifiTracker.{self.name} - {datetime.now()}\n"
            )

    def findBy_class_period(self, room, init_date, final_date):
        try:
            pipeline = [
                {
                    "$match": {
                        "Timestamp": {"$gte": init_date},
                        "Timestamp": {"$lte": final_date},
                        "Room": room,
                    }
                }
            ]
            df_response = pandas.DataFrame(list(self.collection.aggregate(pipeline)))
        except:
            self.error.write(
                f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
            )
        return df_response

    def findLastBy_room(self, room):
        try:
            pipeline = [
                {"$match": {"Room": room}},
                {"$sort": {"_id": -1}},
                {"$limit": 1},
            ]
            df_response = pandas.DataFrame(list(self.collection.aggregate(pipeline)))
        except:
            self.error.write(
                f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
            )
        return df_response

    def findLast_forTracking(self):
        try:
            pipeline = [
                {"$sort": {"_id": -1}},
                {"$limit": 1},
            ]
            df_response = pandas.DataFrame(list(self.collection.aggregate(pipeline)))
            last_timestamp = df_response["Timestamp"].iloc[0]
            df_response = pandas.DataFrame(
                list(self.collection.find({"Timestamp": last_timestamp}))
            )
        except:
            self.error.write(
                f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
            )
        return df_response

    def findBy_period(self, init_date, final_date):
        try:
            pipeline = [
                {
                    "$match": {
                        "Timestamp": {"$gte": init_date},
                        "Timestamp": {"$lte": final_date},
                    }
                }
            ]
            df_response = pandas.DataFrame(list(self.collection.aggregate(pipeline)))
        except:
            self.error.write(
                f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
            )
        return df_response
