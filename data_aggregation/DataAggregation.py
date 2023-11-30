import pandas as pd
from config import *
import re
import parse


class DataAggregation:
    def __init__(self):
        self.myself = "DataAggregation"
        self.error = open(FILE_ERRORS,'w')
        pass

    def aggregate(self):
        """
        The method is used to retrieve the all data contained
        in the files in 'souce_files' folder and to combine
        them in a single DataFrame.
        -----------------------------------------------------
        Output:
            - Dataframe containing all the information 
        """
        self.fill_dataframes()
        self.df_raw_data = self.merge_dataframes()
        self.df_raw_data["domain"] = self.assign_class(self.df_raw_data["domain"])
        self.df_raw_data = self.df_raw_data.rename({"domain": "class"}, axis="columns")
        return self.df_raw_data

    def fill_dataframes(self):
        """
        The method creates a Dataframe for each source file
        """
        self.df_usernames = pd.DataFrame(self.open_username())
        self.rssi = pd.DataFrame(self.open_rssi())
        self.snr = pd.DataFrame(self.open_snr())
        self.byte_rx = pd.DataFrame(self.open_bytes_rx())
        self.byte_tx = pd.DataFrame(self.open_bytes_tx())
        self.ap_mac = pd.DataFrame(self.open_ap_mac())

    def open_username(self):
        """
        The method opens the file containing the username and
        the domain of the user.
        -----------------------------------------------------
        Output:
            - List of dictionaries with the data
        """
        data = []
        with open(FILE_USERNAME, "r") as file_object:
            for i,line in enumerate(file_object):
                try:
                    mac_res = parse.search("iso.3.6.1.4.1.14179.2.1.4.1.3.{} =", line)
                    mac_res = self.convert_hex_notation(mac_res[0])
                    dom_res = parse.search('@{}"', line)[0]
                    username = parse.search('"{}@', line)[0]
                    row = {"mac_user": mac_res, "username": username, "domain": dom_res}
                    data.append(row)
                except:
                    self.error.write(f"Error in {self.myself} - file: '{FILE_USERNAME}' bad formatted, row [{i}]\n")
        return data

    def open_rssi(self):
        """
        The method opens the file containing the rssi value
        of the connection of the user.
        -----------------------------------------------------
        Output:
            - List of dictionaries with the data
        """
        data = []
        with open(FILE_RSSI, "r") as file_object:
            for i,line in enumerate(file_object):
                try:
                    mac_res = parse.search("iso.3.6.1.4.1.14179.2.1.6.1.1.{} =", line)
                    mac_res = self.convert_hex_notation(mac_res[0])
                    rssi_res = parse.search("INTEGER: {:d}", line)[0]
                    row = {
                        "mac_user": mac_res,
                        "rssi": rssi_res,
                    }
                    data.append(row)
                except:
                    self.error.write(f"Error in {self.myself} - file: '{FILE_RSSI}' bad formatted, row [{i}]\n")
        return data

    def open_snr(self):
        """
        The method opens the file containing the snr value of
        the connection of the user.
        -----------------------------------------------------
        Output:
            - List of dictionaries with the data
        """
        data = []
        with open(FILE_SNR, "r") as file_object:
            for i,line in enumerate(file_object):
                try:
                    mac_res = parse.search("iso.3.6.1.4.1.14179.2.1.6.1.26.{} =", line)
                    mac_res = self.convert_hex_notation(mac_res[0])
                    snr_res = parse.search("INTEGER: {:d}", line)[0]
                    row = {
                        "mac_user": mac_res,
                        "snr": snr_res,
                    }
                    data.append(row)
                except:
                    self.error.write(f"Error in {self.myself} - file: '{FILE_SNR}' bad formatted, row [{i}]\n")
        return data

    def open_bytes_rx(self):
        """
        The method opens the file containing the received
        bytes in the connection of the user.
        -----------------------------------------------------
        Output:
            - List of dictionaries with the data
        """
        data = []
        with open(FILE_BYTES_RX, "r") as file_object:
            for i,line in enumerate(file_object):
                try:
                    mac_res = parse.search("iso.3.6.1.4.1.14179.2.1.6.1.3.{} =", line)
                    mac_res = self.convert_hex_notation(mac_res[0])
                    bytes_rx = parse.search("Counter64: {:d}", line)[0]
                    row = {
                        "mac_user": mac_res,
                        "byte_rx": bytes_rx,
                    }
                    data.append(row)
                except:
                    self.error.write(f"Error in {self.myself} - file: '{FILE_BYTES_RX}' bad formatted, row [{i}]\n")
        return data

    def open_bytes_tx(self):
        """
        The method opens the file containing the transmitted
        bytes in the connection of the user.
        -----------------------------------------------------
        Output:
            - List of dictionaries with the data
        """
        data = []
        with open(FILE_BYTES_TX, "r") as file_object:
            for i,line in enumerate(file_object):
                try:
                    mac_res = parse.search("iso.3.6.1.4.1.14179.2.1.6.1.2.{} =", line)
                    mac_res = self.convert_hex_notation(mac_res[0])
                    bytes_tx = parse.search("Counter64: {:d}", line)
                    row = {
                        "mac_user": mac_res,
                        "byte_tx": bytes_tx[0],
                    }
                    data.append(row)
                except:
                    self.error.write(f"Error in {self.myself} - file: '{FILE_BYTES_TX}' bad formatted, row [{i}]\n")
        return data

    def open_ap_mac(self):
        """
        The method opens the file containing the base radio
        mac of the connection of the user.
        -----------------------------------------------------
        Output:
            - List of dictionaries with the data
        """
        data = []
        regex = r"[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}"
        with open(FILE_AP_MAC, "r") as file_object:
            for i,line in enumerate(file_object):
                try:
                    mac_res = parse.search("iso.3.6.1.4.1.14179.2.1.4.1.4.{} =", line)
                    mac_res = self.convert_hex_notation(mac_res[0])
                    ap_mac = re.findall(regex, line)[0]
                    ap_mac = ap_mac.replace(" ", ":").lower()
                    row = {
                        "mac_user": mac_res,
                        "mac_ap": ap_mac,
                    }
                    data.append(row)
                except:
                    self.error.write(f"Error in {self.myself} - file: '{FILE_AP_MAC}' bad formatted, row [{i}]\n")
        return data

    def convert_hex_notation(self, mac_string):
        """
        The method converts the mac address from format
        '\d.\d.\d.\d.\d.\d' to '([0-9a-f]:){5}[0-9a-f]' in 
        hexadecimal
        -----------------------------------------------------
        Parameter:
            - the MAC string formatted
        -----------------------------------------------------
        Output:
            - MAC address formatted
        """
        list_num = mac_string.split(".")
        for i in range(len(list_num)):
            list_num[i] = hex(int(list_num[i]))
        extended_mac = ":".join(list_num)
        return extended_mac.replace("0x", "")

    def merge_dataframes(self):
        """
        The method merges the all dataframes in only one
        -----------------------------------------------------
        Output:
            - the dataframe containing the all data
        """
        result = pd.merge(self.df_usernames, self.rssi, on="mac_user", how="outer")
        result = pd.merge(result, self.snr, on="mac_user", how="outer")
        result = pd.merge(result, self.byte_rx, on="mac_user", how="outer")
        result = pd.merge(result, self.byte_tx, on="mac_user", how="outer")
        return pd.merge(result, self.ap_mac, on="mac_user", how="outer")

    def assign_class(self, domain_list):
        """
        The method gives a class to each user based on the
        domain
        -----------------------------------------------------
        Parameter:
            - the list of domains
        -----------------------------------------------------
        Output:
            - the list of classes assigned
        """
        classes = []
        for domain in domain_list:
            if domain != domain:
                classes.append("Unknown")
            elif domain == "studenti.polito.it":
                classes.append("Students")
            elif domain == "polito.it":
                classes.append("Professor")
            else:
                classes.append("External")
        return classes
