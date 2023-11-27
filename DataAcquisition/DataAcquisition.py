import os
from config import *


class DataAcquisition:
    """
    DataAcquisition
    ---------------
    Deals with the acquisition of the data through SNMP query.\\
    All the data will be saved on files in SNMP_Files folder.
    """

    def __init__(self):
        pass

    def acquier(self):
        """
        acquier
        -------
        Obtain the data that will be obtained more frequently, like\\
        MAC, username, snr of device connected in this moment at the AP.
        """
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
        """
        acquier_AP
        ----------
        Useful data for the position and name of the AP.\\
        Can be requested few time, like one a day.
        """
        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} {OID_AP_WEB} > SNMP_Files/{FILE_AP_WEB}"
        )

        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} {OID_AP_NAME} > SNMP_Files/{FILE_AP_NAME}"
        )
