import pandas
from .config import *
import datetime
import time


class mongo_library:

    def __init__(self, coll, name):
        self.collection = coll
        self.name = name
        self.error = open(FILE_ERRORS, "w")

    def getName(self):
        return self.collection

    def insert_records(self, df):
        """
        insert_records
        --------------
        Insert the data received in the specific collection of the mongoDB instance
        """
        if self.name == COUNTNAME:
            self.insert_count(df)
        elif self.name == TRACKNAME:
            self.insert_track(df)
        elif self.name == RAWNAME:
            self.insert_raw(df)

    def insert_count(self, df):
        if len(df) > 1:
            try:
                dict = df.T.to_dict().values()
                self.collection.insert_many(dict)
            except:
                self.error.write(
                    f"Connection error: wifiTracker.{self.name} unreachable - {datetime.datetime.now()}\n"
                )
        else:
            try:
                dict = df.to_dict()
                self.collection.insert_one(dict)
            except:
                self.error.write(
                    f"Connection error: wifiTracker.{self.name} unreachable - {datetime.datetime.now()}\n"
                )

    def insert_track(self, df):
        if len(df) > 1:
            try:
                timestamp = time.time()
                for index, row in df.iterrows():
                    destination = []
                    for room, people in row.items():
                        if people != 0:
                            destination.append((room, people))
                    dict = {
                        "From": index,
                        "To": destination,
                        "Timestamp": timestamp,
                    }
                    self.collection.insert_one(dict)
            except:
                self.error.write(
                    f"Connection error: wifiTracker.{self.name} unreachable - {datetime.datetime.now()}\n"
                )

    def insert_raw(self, df):
        """Since raw data will weight a lot, MongoDB will delete the old files
        saved after a specific time set to 2 month. To change this time is
        necessary to connect to the VM running the code and change it via
        the mongo Shell of the local mongoDB server."""
        if len(df) > 1:
            try:
                df["Timestamp"] = datetime.datetime.now()
                dict = df.T.to_dict().values()
                self.collection.insert_many(dict)
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
                f"Connection error: wifiTracker.{self.name} unreachable - {datetime.datetime.now()}\n"
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
                f"Connection error: wifiTracker.{self.name} unreachable - {datetime.datetime.now()}\n"
            )
        return df_response
