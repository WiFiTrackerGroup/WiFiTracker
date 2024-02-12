# IP and PORT od the SNMP rest interface
IP = "127.0.0.1"
PORT = "8282"

# Seconds to wait before asking anothe acquisition
SCHEDULE = 15

# MONGODB config
PSW_MONGODB = "ciao"
USER_MONGODB = "wifitracker2024"

DBNAME = "WifiTracker2024"
COUNTNAME = "countingPerTimeClass"
TRACKNAME = "tracking"

URL_DB = (
    f"mongodb+srv://wifitracker2024:{PSW_MONGODB}@{USER_MONGODB}.fqyv89v.mongodb.net/"
)

FILE_ERRORS = "Service/sub/log/mongoDB_log.txt"
