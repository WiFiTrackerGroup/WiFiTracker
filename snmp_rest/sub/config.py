# Configuration file

# IP and Port of the rest interface
IP = "127.0.0.1"
PORT = 8282

# Bytes dimension of salt used in hashing
N_BYTES = 16
# Salt time window update
T_UPD_SALT = 20

# Set hour when salt is changed every day
HOUR_SALT = "00:30"

# Set hout when AP names are retrieved every day
HOUR_AP = "00:35"

# Buffer value for near response
TIME_BUFF = 59

# snmpwalk command information
COMMUNITY = "-c abcdefghi"
IP_WLC = "130.192.xx.yy"
OID_MAC = "3.6.1.4.1.14179.2.1.4.1.1"
OID_USERNAME = "3.6.1.4.1.14179.2.1.4.1.3"
OID_RSSI = "3.6.1.4.1.14179.2.1.6.1.1"
OID_SNR = "3.6.1.4.1.14179.2.1.6.1.26"
OID_BYTES_TX = "3.6.1.4.1.14179.2.1.6.1.2"
OID_BYTES_RX = "3.6.1.4.1.14179.2.1.6.1.3"
OID_AP_MAC = "3.6.1.4.1.14179.2.1.4.1.4"
OID_AP_WEB = "3.6.1.4.1.9.9.513.1.2.3.1.1"
OID_AP_NAME = "3.6.1.4.1.9.9.513.1.1.1.1.5"

# new oid commands
OID_PRIMARY_CH = "3.6.1.4.1.14179.2.2.2.1.4"
OID_CHANNEL_UTIL = "3.6.1.4.1.14179.2.2.13.1.3"
OID_NOISE = "3.6.1.4.1.14179.2.2.15.1.21"
OID_POWER_TX = "3.6.1.4.1.14179.2.2.2.1.6"
OID_N_CLIENT = "3.6.1.4.1.14179.2.2.2.1.15"
OID_CLIENT_TYPE = "3.6.1.4.1.9.9.599.1.3.1.1.6"


# SNMP files names directory
FILE_MAC = "snmp_data/mac.txt"
FILE_USERNAME = "snmp_data/username.txt"
FILE_RSSI = "snmp_data/rssi.txt"
FILE_SNR = "snmp_data/snr.txt"
FILE_BYTES_TX = "snmp_data/bytes_tx.txt"
FILE_BYTES_RX = "snmp_data/bytes_rx.txt"
FILE_AP_MAC = "snmp_data/ap_mac.txt"
FILE_AP_WEB = "snmp_data/ap_web.txt"
FILE_AP_NAME = "snmp_data/ap_name.txt"
# for new OID
FILE_PRIMARY_CH = "snmp_data/primary_ch.txt"
FILE_CHANNEL_UTIL = "snmp_data/channel_util.txt"
FILE_NOISE = "snmp_data/noise.txt"
FILE_POWER_TX = "snmp_data/power_tx.txt"
FILE_N_CLIENT = "snmp_data/n_client.txt"
FILE_CLIENT_TYPE = "snmp_data/client_type.txt"

# File error file directory
FILE_ERRORS = "logs/error_log.txt"
