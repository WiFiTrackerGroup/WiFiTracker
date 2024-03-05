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

        # Collection
        self.myDB = self.myclient[DBNAME]
        self.myCount = mongo_library(self.myDB[COUNTNAME], COUNTNAME)
        self.myTrack = mongo_library(self.myDB[TRACKNAME], TRACKNAME)

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

    def save_history(self, data):
        """
        save_history
        ------------
        save as history all the data obtained from the rest interface
        """
        x = dt.fromtimestamp(data["Timestamp"].iloc[0])
        path = FILE_HISTORY + x.strftime("%d_%m_%Y_%H_%M_%S") + ".csv"
        data.to_csv(path)

    def data_clean(self):
        """
        data_clean
        ----------
        clean routine for old files
        """
        current_time = time.time()
        for i, file in enumerate(os.listdir(FILE_HISTORY)):
            file_time = os.stat(FILE_HISTORY + file).st_mtime
            if file_time < current_time - DAY * N_DAY:
                os.remove(FILE_HISTORY + file)

    def request(self):
        """
        request
        -------
        Request every SCHEDULE seconds the rooms information
        """
        try:
            print("Starting data retrieval...")
            req_data = requests.get(self.SNMPaddr + "/data")
            print("Data retrieved successfully!")
        except:
            raise Exception("Error occured during server request!")

        if req_data.ok:
            dataRoom = pd.DataFrame.from_dict(req_data.json())
            self.save_history(data=dataRoom)
            # Counting people
            dataCount = self.countP.main(dataRoom)
            self.myCount.insert_records(dataCount)
            # Tracking people
            if not self.df_t_1.empty:
                dataTrack = self.track.eval_od_matrix(self.df_t_1, dataRoom)
                self.myTrack.insert_records(dataTrack)
            # DF at t-1 needed for tracking purpose
            self.df_t_1 = dataRoom.copy()

    def main(self):

        schedule.every(SCHEDULE).seconds.do(self.request)
        schedule.every().day.at("02:00").do(self.data_clean)
        try:
            while True:
                schedule.run_pending()
                time.sleep(5)
        except KeyboardInterrupt:
            raise Exception("Program interrupted")


if __name__ == "__main__":
    aq = Acquisition()
    aq.main()
