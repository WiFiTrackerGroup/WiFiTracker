import time
import pandas as pd
import schedule
import requests
from sub.config import *
from sub.counting_people import *


class Acquisition:
    def __init__(self):
        self.SNMPaddr = "http://" + IP + ":" + PORT

        # When started the first thing to do is obtain APdata
        self.requestAP()

        # Initialization
        self.countP = Counting_P()

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
        try:
            req_data = requests.get(self.SNMPaddr + "/data")
            if req_data.ok:
                dataRoom = pd.DataFrame.from_dict(req_data.json())
                self.countP.main(dataRoom)
        except:
            raise Exception

    def main(self):
        schedule.every().day.at(HOUR).do(self.requestAP)
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
