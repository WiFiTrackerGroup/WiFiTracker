import os
import time
import pandas as pd
import schedule
import requests
import pymongo as pm
from datetime import datetime as dt
from sub.config import *
from sub.counting_people import *
from sub.mongoDB_library import *
from sub.tracking import tracking


class Acquisition:
    def __init__(self):
        self.SNMPaddr = "http://" + IP + ":" + PORT

        # Initialization
        self.countP = Counting_P()
        self.track = tracking()
        self.myclient = pm.MongoClient(URL_DB)
        self.df_t_1 = pd.DataFrame()  # containing data of the previous request
        self.old_hour = -1

        # Collection
        self.myDB = self.myclient[DBNAME]
        self.myCount = mongo_library(self.myDB[COUNTNAME], COUNTNAME)
        self.myTrack = mongo_library(self.myDB[TRACKNAME], TRACKNAME)
        self.myRaw = mongo_library(self.myDB[RAWNAME], RAWNAME)

    def requestAP(self):
        """
        requestAP
        ---------
        Request once a day and at the start of the program the AP information
        """
        try:
            req_AP = requests.get(self.SNMPaddr + "/AP")
            if req_AP.ok:
                APdata = req_AP.json()
        except:
            print("SNMP server not accessible")

    def request(self):
        """
        request
        -------
        Request every SCHEDULE seconds the rooms information
        """
        if self.check_time():
            try:
                if PRINT:
                    print("Starting data retrieval...")
                req_data = requests.get(self.SNMPaddr + "/data")
                if PRINT:
                    print("Data retrieved successfully!")
            except:
                print("Exception! Error occured during server request!")

            if req_data.ok:
                dataRoom = pd.DataFrame.from_dict(req_data.json())
                if len(dataRoom) > 0:
                    self.myRaw.insert_records(dataRoom)
                    # Counting people
                    dataCount = self.countP.main(dataRoom)
                    # The saving is done only if there are people in the rooms
                    if len(dataCount) > 0:
                        self.myCount.insert_records(dataCount)
                        # Tracking people
                        if not self.df_t_1.empty:
                            dataTrack = self.track.eval_od_matrix(self.df_t_1, dataRoom)
                            self.myTrack.insert_records(dataTrack)
                        # DF at t-1 needed for tracking purpose
                        self.df_t_1 = dataRoom.copy()
                    else:
                        self.df_t_1 = self.df_t_1.iloc[0:0]

    def check_time(self):
        """
        check_time
        ----------
        Check the time to compare it with config parameters.
        During night we want that the acquisition will work less.
        """
        hour = time.localtime().tm_hour
        if hour >= TIME_REDUCE or hour <= TIME_INCREASE:
            if hour == self.old_hour:
                return False
            else:
                self.old_hour = hour
                return True
        else:
            return True

    def main(self):

        schedule.every(SCHEDULE).seconds.do(self.request)
        try:
            while True:
                schedule.run_pending()
                time.sleep(5)
        except KeyboardInterrupt:
            raise Exception("Program interrupted")


if __name__ == "__main__":
    aq = Acquisition()
    aq.main()
