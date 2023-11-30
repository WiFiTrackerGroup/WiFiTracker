IP = "0.0.0.0"
PORT = 8080

# Bytes dimension of salt used in hashing
N_BYTES = 16
# Salt time window update
T_UPD_SALT = 20

# Configuration file

# snmpwalk command information
COMMUNITY = "-c abcdefghi"
IP_WLC = "130.192.xx.yy"
OID_MAC = "1.3.6.1.4.1.14179.2.1.4.1.1"
OID_USERNAME = "1.3.6.1.4.1.14179.2.1.4.1.3"
OID_RSSI = "1.3.6.1.4.1.14179.2.1.6.1.1"
OID_SNR = "1.3.6.1.4.1.14179.2.1.6.1.26"
OID_BYTES_TX = "1.3.6.1.4.1.14179.2.1.6.1.2"
OID_BYTES_RX = "1.3.6.1.4.1.14179.2.1.6.1.3"
OID_AP_MAC = "1.3.6.1.4.1.14179.2.1.4.1.4"
OID_AP_WEB = "1.3.6.1.4.1.9.9.513.1.2.3.1.1"
OID_AP_NAME = "1.3.6.1.4.1.9.9.513.1.1.1.1.5"

# Files names
FILE_MAC = "SNMP_REST/snmp_data/mac.txt"
FILE_USERNAME = "SNMP_REST/snmp_data/username.txt"
FILE_RSSI = "SNMP_REST/snmp_data/rssi.txt"
FILE_SNR = "SNMP_REST/snmp_data/snr.txt"
FILE_BYTES_TX = "SNMP_REST/snmp_data/bytes_tx.txt"
FILE_BYTES_RX = "SNMP_REST/snmp_data/bytes_rx.txt"
FILE_AP_MAC = "SNMP_REST/snmp_data/ap_mac.txt"
FILE_AP_WEB = "SNMP_REST/snmp_data/ap_web.txt"
FILE_AP_NAME = "SNMP_REST/snmp_data/ap_name.txt"

FILE_ERRORS = "SNMP_REST/sub/logs/error_log.txt"
