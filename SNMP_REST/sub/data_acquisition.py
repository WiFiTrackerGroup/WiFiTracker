import os
from .config import *


class DataAcquisition:
    """
    DataAcquisition
    ---------------
    Deals with the acquisition of the data through SNMP query.\\
    All the data will be saved on files in snmp_data folder.
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
        os.system(f"snmpwalk -v2c {COMMUNITY} {IP_WLC} 1.{OID_MAC} > {FILE_MAC}")

        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} 1.{OID_USERNAME} > {FILE_USERNAME}"
        )

        os.system(f"snmpwalk -v2c {COMMUNITY} {IP_WLC} 1.{OID_RSSI} > {FILE_RSSI}")

        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} 1.{OID_BYTES_TX} > {FILE_BYTES_TX}"
        )

        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} 1.{OID_BYTES_RX} > {FILE_BYTES_RX}"
        )

        os.system(f"snmpwalk -v2c {COMMUNITY} {IP_WLC} 1.{OID_AP_MAC} > {FILE_AP_MAC}")

    def acquier_AP(self):
        """
        acquier_AP
        ----------
        Useful data for the position and name of the AP.\\
        Can be requested few time, like one a day.
        """
        os.system(f"snmpwalk -v2c {COMMUNITY} {IP_WLC} 1.{OID_AP_WEB} > {FILE_AP_WEB}")

        os.system(
            f"snmpwalk -v2c {COMMUNITY} {IP_WLC} 1.{OID_AP_NAME} > {FILE_AP_NAME}"
        )
