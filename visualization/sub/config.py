# IP and PORT od the SNMP rest interface
IP = "192.168.67.41"
PORT = "8282"

# Seconds to wait before asking another acquisition
SCHEDULE = 900
TRACKING_TIME = 6 * SCHEDULE  # time in seconds
PRINT = False

# MONGODB config
DBNAME = "WifiTracker2024"
COUNTNAME = "counting"
TRACKNAME = "tracking"
RAWNAME = "raw_data"
INPUTNAME = "input_count"

# ----------------------------------------------------------------------------------------
# Config for local mongoDB
PSW_MONGODB = ""  # to be inserted
USER_MONGODB = "root"
HOST_MONGODB = "127.0.0.1"
PORT_MONGODB = "27017"
URL_DB = f"mongodb://{USER_MONGODB}:{PSW_MONGODB}@{HOST_MONGODB}:{PORT_MONGODB}"
# ----------------------------------------------------------------------------------------

FILE_ERRORS = "sub/log/mongoDB_log.txt"

# Set the hours when to reduce the acquisition
# Default : 21
TIME_REDUCE = 21
# Default : 7
TIME_INCREASE = 7
