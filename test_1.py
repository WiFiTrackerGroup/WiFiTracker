import pymongo as pm
import pandas

uri = "mongodb://readCounting:@mongo_server_ip:27017"
client = pm.MongoClient("mongodb://root:ciao@wifitrack.polito.it:8502")
# client = pymongo.MongoClient("mongodb://root:ciao@130.192.238.41:27017")
# defaults to port 27017,
db = client["WifiTracker2024"]
print(pandas.DataFrame(list(db.counting.find({}).limit(4))))
