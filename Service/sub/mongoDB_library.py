import pandas
from sub.config import *
from datetime import datetime, timedelta
import time


class mongo_library:

    def __init__(self, coll, name):
        self.collection = coll
        self.name = name
        self.error = open(FILE_ERRORS, "w")

    def getName(self):
        return self.name

    # ------------------------------------------------------------------------------
    # INSERTION METHODS
    # ------------------------------------------------------------------------------
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

    def insert_track(self, df):
        if len(df) > 1:
            try:
                timestamp = datetime.now()
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
                    f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
                )

    def insert_raw(self, df):
        """
        Since raw data will weight a lot, MongoDB will delete the old files
        saved after a specific time set to 2 month. To change this time is
        necessary to connect to the VM running the code and change it via
        the mongo Shell of the local mongoDB server.
        """
        if len(df) > 1:
            try:
                df["Timestamp"] = datetime.now()
                dict = df.T.to_dict().values()
                self.collection.insert_many(dict)
            except:
                self.error.write(
                    f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
                )
        else:
            self.error.write(
                f"Wrong collection contacted: wifiTracker.{self.name} - {datetime.now()}\n"
            )

    def insert_true_value(self, df):
        """
        insert_true_value
        -----------------
        Insertion query used to send data of the true value of people counted in a room.
        Send to the collection:
        - The true number of people
        - The room in which the people are counted
        - The timestamp
        """

        try:
            self.collection.insert_one(df)
            return True
        except:
            self.error.write(
                f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
            )
            return False

    # ------------------------------------------------------------------------------
    # FIND METHODS
    # ------------------------------------------------------------------------------

    def findBy_room_period(self, room, init_date, final_date):
        """
        findBy_room_period
        ------------------
        The method returns the records associated to a room for a period of time.
        It can be called on the "counting" collection.
        Input:
            - room: string with the name of the room
            - init_date
            - final_date
        Output:
            - df_response: dataframe
        """
        if self.name == COUNTNAME:
            try:
                pipeline = [
                    {
                        "$match": {
                            "Timestamp": {"$gte": init_date, "$lte": final_date},
                            "Room": room,
                        }
                    }
                ]
                df_response = pandas.DataFrame(
                    list(self.collection.aggregate(pipeline))
                )
            except:
                self.error.write(
                    f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
                )
        else:
            self.error.write(
                f"Wrong collection contacted: wifiTracker.{self.name} - {datetime.now()}\n"
            )
        return df_response

    def findBy_room_timestamp(self, room, timestamp):
        """
        findBy_room_timestamp
        ---------------------
        The method returns the closest record to the selected timestamp related
        to the choosen room. The method works only on the "counting" collection.
        Input:
            - room: string with the name of the room
            - timestamp
        Output:
            - df_response: it is a dataframe with one row only
        """
        if self.name == COUNTNAME:
            try:
                timestamp_before = timestamp - timedelta(seconds=SCHEDULE)
                timestamp_after = timestamp + timedelta(seconds=SCHEDULE)
                pipeline = [
                    {
                        "$match": {
                            "Timestamp": {
                                "$gte": timestamp_before,
                                "$lte": timestamp_after,
                            },
                            "Room": room,
                        }
                    },
                    {
                        "$project": {
                            "Room": 1,
                            "Timestamp": 1,
                            "N_people": 1,
                            "_id": 1,
                            "time_dist": {
                                "$abs": [{"$subtract": ["$Timestamp", timestamp]}]
                            },
                        }
                    },
                    {"$sort": {"time_dist": 1}},
                    {"$limit": 1},
                ]
                df_response = pandas.DataFrame(
                    list(self.collection.aggregate(pipeline))
                )
            except:
                self.error.write(
                    f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
                )
        else:
            self.error.write(
                f"Wrong collection contacted: wifiTracker.{self.name} - {datetime.now()}\n"
            )
        return df_response

    def findLastBy_room(self, room):
        """
        findLastBy_room
        ---------------
        The method returns the last record of the room selected. It can be
        called on the "counting" collection.
        Input:
            - room: string with the name of the room
        Output:
            - df_response: it is a dataframe with one row only
        """
        if self.name == COUNTNAME:
            try:
                pipeline = [
                    {"$match": {"Room": room}},
                    {"$sort": {"_id": -1}},
                    {"$limit": 1},
                ]
                df_response = pandas.DataFrame(
                    list(self.collection.aggregate(pipeline))
                )
            except:
                self.error.write(
                    f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
                )
        else:
            self.error.write(
                f"Wrong collection contacted: wifiTracker.{self.name} - {datetime.now()}\n"
            )
        return df_response

    def findLast_forTracking(self):
        """
        findLast_forTracking
        --------------------
        The method returns the records associated with the last timestamp. It
        can be called on the "tracking" collection.
        Input:
            - room: string with the name of the room
        Output:
            - df_response: it is a dataframe with one row only
        """
        if self.name == TRACKNAME:
            try:
                pipeline = [
                    {"$sort": {"_id": -1}},
                    {"$limit": 1},
                ]
                df_response = pandas.DataFrame(
                    list(self.collection.aggregate(pipeline))
                )
                last_timestamp = df_response["Timestamp"].iloc[0]
                df_response = pandas.DataFrame(
                    list(self.collection.find({"Timestamp": last_timestamp}))
                )
            except:
                self.error.write(
                    f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
                )
        else:
            self.error.write(
                f"Wrong collection contacted: wifiTracker.{self.name} - {datetime.now()}\n"
            )
        return df_response

    def findTimestamp_forTracking(self, timestamp):
        """
        findPeriod_forTracking
        ----------------------
        The method returns the closest record to the timestamp passed. It can be
        called on the "tracking" collection.
        Input:
            - timestamp
        Output:
            - df_response
        """
        if self.name == TRACKNAME:
            try:
                timestamp_before = timestamp - timedelta(seconds=(SCHEDULE * 6))
                timestamp_after = timestamp + timedelta(seconds=(SCHEDULE * 6))
                pipeline = [
                    {
                        "$match": {
                            "Timestamp": {
                                "$gte": timestamp_before,
                                "$lte": timestamp_after,
                            },
                        }
                    },
                    {
                        "$project": {
                            "Timestamp": 1,
                            "time_dist": {
                                "$abs": [{"$subtract": ["$Timestamp", timestamp]}]
                            },
                        }
                    },
                    {"$sort": {"time_dist": 1}},
                    {"$limit": 1},
                ]
                df_response = pandas.DataFrame(
                    list(self.collection.aggregate(pipeline))
                )
                last_timestamp = df_response["Timestamp"].iloc[0]
                df_response = pandas.DataFrame(
                    list(self.collection.find({"Timestamp": last_timestamp}))
                )
            except:
                self.error.write(
                    f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
                )
        else:
            self.error.write(
                f"Wrong collection contacted: wifiTracker.{self.name} - {datetime.now()}\n"
            )
        return df_response

    def findRawDataBy_period(self, init_date, final_date):
        """
        findRawDataBy_period
        --------------------
        The method returns the records in a period of time. It can be called on
        the "raw_data" collection only.
        Input:
            - init_date
            - final_date
        Output:
            - df_response: dataframe
        """
        if self.name == RAWNAME:
            try:
                pipeline = [
                    {
                        "$match": {
                            "Timestamp": {"$gte": init_date, "$lte": final_date},
                        }
                    }
                ]
                df_response = pandas.DataFrame(
                    list(self.collection.aggregate(pipeline))
                )
            except:
                self.error.write(
                    f"Connection error: wifiTracker.{self.name} unreachable - {datetime.now()}\n"
                )
        else:
            self.error.write(
                f"Wrong collection contacted: wifiTracker.{self.name} - {datetime.now()}\n"
            )
        return df_response
