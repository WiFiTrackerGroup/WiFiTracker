import pymongo as pm
import pandas

uri = "mongodb://readCounting:@mongo_server_ip:27017"
client = pm.MongoClient("mongodb://root:ciao@130.192.238.41:27017")
# client = pymongo.MongoClient("mongodb://root:ciao@130.192.238.41:27017")
# defaults to port 27017,
db = client["WifiTracker2024"]
db.counting.insert_one({"ciao":3, "casa":4})
