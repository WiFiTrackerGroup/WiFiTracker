import pandas as pd
from config import *
import re
import parse
import numpy as np


class DataAggregation:
    def __init__(self):
        pass

    def aggregate(self):
        self.fill_dataframes()
        self.df_raw_data = self.merge_dataframes()
        self.df_raw_data["domain"] = self.assign_class(self.df_raw_data["domain"])
        self.df_raw_data = self.df_raw_data.rename({"domain": "class"}, axis="columns")
        return self.df_raw_data

    def fill_dataframes(self):
        self.df_usernames = pd.DataFrame(self.open_username())
        self.rssi = pd.DataFrame(self.open_rssi())
        self.snr = pd.DataFrame(self.open_snr())
        self.byte_rx = pd.DataFrame(self.open_bytes_rx())
        self.byte_tx = pd.DataFrame(self.open_bytes_tx())
        self.ap_mac = pd.DataFrame(self.open_ap_mac())
        print(self.ap_mac)

    def open_username(self):
        data = []
        with open(FILE_USERNAME, "r") as file_object:
            for line in file_object:
                if self.file_check(line):
                    mac_res = parse.search("iso.3.6.1.4.1.14179.2.1.4.1.3.{} =", line)[
                        0
                    ]
                    mac_res = hex(int(mac_res.replace(".", "")))
                    dom_res = parse.search('@{}"', line)[0]

                    username = parse.search('"{}@', line)[0]
                    row = {"mac": mac_res, "username": username, "domain": dom_res}
                    data.append(row)
        return data

    def open_rssi(self):
        data = []
        with open(FILE_RSSI, "r") as file_object:
            for line in file_object:
                if self.file_check(line):
                    mac_res = parse.search("iso.3.6.1.4.1.14179.2.1.6.1.1.{} =", line)[
                        0
                    ]
                    mac_res = hex(int(mac_res.replace(".", "")))
                    rssi_res = parse.search("INTEGER: {:d}", line)[0]
                    row = {
                        "mac": mac_res,
                        "rssi": rssi_res,
                    }
                    data.append(row)
        return data

    def open_snr(self):
        data = []
        with open(FILE_SNR, "r") as file_object:
            for line in file_object:
                if self.file_check(line):
                    mac_res = parse.search("iso.3.6.1.4.1.14179.2.1.6.1.26.{} =", line)[
                        0
                    ]
                    mac_res = hex(int(mac_res.replace(".", "")))
                    snr_res = parse.search("INTEGER: {:d}", line)[0]
                    row = {
                        "mac": mac_res,
                        "snr": snr_res,
                    }
                    data.append(row)
        return data

    def open_bytes_rx(self):
        data = []
        with open(FILE_BYTES_RX, "r") as file_object:
            for line in file_object:
                if self.file_check(line):
                    mac_res = parse.search("iso.3.6.1.4.1.14179.2.1.6.1.3.{} =", line)[
                        0
                    ]
                    mac_res = hex(int(mac_res.replace(".", "")))
                    bytes_rx = parse.search("Counter64: {:d}", line)[0]
                    row = {
                        "mac": mac_res,
                        "byte_rx": bytes_rx,
                    }
                    data.append(row)
        return data

    def open_bytes_tx(self):
        data = []
        with open(FILE_BYTES_TX, "r") as file_object:
            for line in file_object:
                if self.file_check(line):
                    mac_res = parse.search("iso.3.6.1.4.1.14179.2.1.6.1.2.{} =", line)[0]
                    mac_res = hex(int(mac_res.replace(".", "")))
                    bytes_tx = parse.search("Counter64: {:d}", line)[0]
                    row = {
                        "mac": mac_res,
                        "byte_tx": bytes_tx,
                    }
                    data.append(row)
        return data
    
    def open_ap_mac(self):
        data = []
        regex = "([0-9A-Fa-f]{2}[\s]){5}([0-9A-Fa-f]{2})"
        with open(FILE_AP_MAC, "r") as file_object:
            for line in file_object:
                if self.file_check(line):
                    mac_res = parse.search("iso.3.6.1.4.1.14179.2.1.4.1.4.{} =", line)[0]
                    mac_res = hex(int(mac_res.replace(".", "")))
                    ba_mac = re.findall(regex, line)
                    row = {
                        "mac": mac_res,
                        "byte_tx": ba_mac,
                    }
                    data.append(row)
        return data

    def file_check(self, line):
        if line.startswith("iso", 0, 3):
            return True
        else:
            return False

    def merge_dataframes(self):
        result = pd.merge(self.df_usernames, self.rssi, on="mac", how="outer")
        result = pd.merge(result, self.snr, on="mac", how="outer")
        result = pd.merge(result, self.byte_rx, on="mac", how="outer")
        return pd.merge(result, self.byte_tx, on="mac", how="outer")

    def assign_class(self, domain_list):
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


elem = DataAggregation()
elem.aggregate()
