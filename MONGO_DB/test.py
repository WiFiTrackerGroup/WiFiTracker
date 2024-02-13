import time
import pandas as pd

import pymongo as pm
from config import *



class Acquisition:
    def __init__(self):
        self.myclient = pm.MongoClient(URL_DB)

        # DB
        self.myDB = self.myclient[DBNAME]
        self.collection = self.myDB[COUNTNAME]

        self.collection.insert_one({"ciao":"1", "bella":"4"})

if __name__ == "__main__":
    mongo = Acquisition()
        
