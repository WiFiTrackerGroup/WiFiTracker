import os
from DataAcquisition.config import *


class DataAcquisition:
    def __init__(self):
        pass

    def acquier(self):
        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} {OID_MAC} > SNMP_Files/{FILE_MAC}"
        )

        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} {OID_USERNAME} > SNMP_Files/{FILE_USERNAME}"
        )

        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} {OID_RSSI} > SNMP_Files/{FILE_RSSI}"
        )

        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} {OID_BYTES_TX} > SNMP_Files/{FILE_BYTES_TX}"
        )

        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} {OID_BYTES_RX} > SNMP_Files/{FILE_BYTES_RX}"
        )

        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} {OID_AP_MAC} > SNMP_Files/{FILE_AP_MAC}"
        )

    def acquier_AP(self):
        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} {OID_AP_WEB} > SNMP_Files/{FILE_AP_WEB}"
        )

        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} {OID_AP_NAME} > SNMP_Files/{FILE_AP_NAME}"
        )
