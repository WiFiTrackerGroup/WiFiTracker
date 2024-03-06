# IP and PORT od the SNMP rest interface
IP = "127.0.0.1"
PORT = "8282"

# Seconds to wait before asking anothe acquisition
SCHEDULE = 10

# MONGODB config

DBNAME = "WifiTracker2024"
COUNTNAME = "counting"
TRACKNAME = "tracking"

# ----------------------------------------------------------------------------------------
# Config for local mongoDB
PSW_MONGODB = "hcgFRD3G!f"
USER_MONGODB = "wifitracker"
HOST_MONGODB = "127.0.0.1"
PORT_MONGODB = "27017"
URL_DB = f"mongodb://{USER_MONGODB}:{PSW_MONGODB}@{HOST_MONGODB}:{PORT_MONGODB}/{DBNAME}"
# ----------------------------------------------------------------------------------------

FILE_ERRORS = "Service/sub/log/mongoDB_log.txt"
FILE_HISTORY = "Service/history/"

# "day" is the number of seconds in a day
DAY = 100
# Number of day to keep the files
N_DAY = 1
