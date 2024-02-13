# IP and PORT od the SNMP rest interface
IP = "127.0.0.1"
PORT = "8282"

# Seconds to wait before asking anothe acquisition
SCHEDULE = 10

# MONGODB config
PSW_MONGODB = "test"
USER_MONGODB = "test"

DBNAME = "test"
COUNTNAME = "test"
TRACKNAME = "tracking"

URL_DB = (
    f"mongodb+srv://{USER_MONGODB}:{PSW_MONGODB}@wifitracker2024.fqyv89v.mongodb.net/"
)

FILE_ERRORS = "Service/sub/log/mongoDB_log.txt"
