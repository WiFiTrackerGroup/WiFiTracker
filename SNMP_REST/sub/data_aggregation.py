import pandas as pd
from functools import reduce
from .config import *
import re
import parse


class DataAggregation:
    def __init__(self):
        self.myself = "DataAggregation"
        self.error = open(FILE_ERRORS, "w")

    def aggregate(self):
        """
        aggregate
        ---------
        The method is used to retrieve the data contained in the files stored in \\
        'snmp_data' folder related to a connection and to combine them in a DataFrame.
        ### Output:
            - Dataframe containing all the information
        """
        try:
            self.dict_ap_aggregate
        except AttributeError:
            self.aggregate_AP()

        self.fill_dataframes()
        self.df_raw_data = self.merge_dataframes()
        self.df_raw_data["class"] = self.assign_class(self.df_raw_data["domain"])
        return self.df_raw_data

    def aggregate_AP(self):
        """
        aggregate_AP
        ------------
        The method retrieves the data related to the access
        points of PoliTO and combines them in a dictionary.
        ### Output
            - The Dataframe containing the mac and the name
            of the APs
        """
        self.ap_web = pd.DataFrame(self.open_ap_web())
        self.ap_web = self.ap_web.drop_duplicates()
        self.ap_name = pd.DataFrame(self.open_ap_name())
        self.ap_name = self.ap_name.drop_duplicates()
        df_ap_aggregate = pd.merge(self.ap_web, self.ap_name, on="code_ap", how="outer")
        df_ap_aggregate = df_ap_aggregate.set_index("mac_ap")[["name_ap", "code_ap"]]
        self.dict_ap_aggregate = df_ap_aggregate.to_dict()
        return df_ap_aggregate

    def aggregate_channel_info(self):
        """
        aggregate_channel_info
        -----------
        Retrieves the channels information of APs and combines
        them with the previously created access points dictionary
        ### Output
            - Dataframe containg AP mac, name and channels info
        """
        try:
            self.dict_ap_aggregate
        except AttributeError:
            self.aggregate_AP()
        # Buffer dataframe to concatenate new columns
        df_aggr_buff = pd.DataFrame()
        self.prim_channels = pd.DataFrame(self.open_primary_channels())
        df_aggr_buff = pd.merge(
            pd.DataFrame.from_dict(self.dict_ap_aggregate),
            self.prim_channels,
            on="code_ap",
            how="outer",
        )
        self.chann_utilization = pd.DataFrame(self.open_channel_utilization())
        df_aggr_buff = pd.merge(
            df_aggr_buff, self.chann_utilization, on="code_ap", how="outer"
        )
        """ self.noise = pd.DataFrame(self.open_noise())
        df_aggr_buff = pd.merge(
            df_aggr_buff,
            self.noise,
            on=["code_ap", "channel_1"],
            how="outer",
        )
        df_aggr_buff = pd.merge(
            df_aggr_buff,
            self.noise,
            on=["code_ap", "channel_2"],
            how="outer",
        ) """
        self.tx_power = pd.DataFrame(self.open_tx_power())
        # TODO:ignorare valore se banda non attiva
        df_aggr_buff = pd.merge(df_aggr_buff, self.tx_power, on="code_ap", how="outer")
        self.clients_on_channel = pd.DataFrame(self.open_client_on_channel())
        df_aggr_buff = pd.merge(
            df_aggr_buff, self.clients_on_channel, on="code_ap", how="outer"
        )
        return df_aggr_buff

    def fill_dataframes(self):
        """
        fill_dataframes
        ---------------
        The method creates a Dataframe for each source file
        """
        self.df_usernames = pd.DataFrame(self.open_username())
        self.rssi = pd.DataFrame(self.open_rssi())
        self.snr = pd.DataFrame(self.open_snr())
        self.byte_rx = pd.DataFrame(self.open_bytes_rx())
        self.byte_tx = pd.DataFrame(self.open_bytes_tx())
        self.client_type = pd.DataFrame(self.open_client_type())
        self.ap_mac = pd.DataFrame(self.open_ap_mac())

    def open_username(self):
        """
        open_username
        -------------
        The method opens the file containing the username and
        the domain of the user.
        ### Output:
            - List of dictionaries with the data
        """
        data = []
        with open(FILE_USERNAME, "r") as file_object:
            for i, line in enumerate(file_object):
                try:
                    mac_res = parse.search(f"iso.{OID_USERNAME}.{{}} =", line)
                    mac_res = self.convert_hex_notation(mac_res[0])
                    dom_res = parse.search('@{}"', line)[0]
                    username = parse.search('"{}@', line)[0]
                    if re.match(r"^[gG]\d+$", username) and dom_res == "polito.it":
                        dom_res = "polito.guest"
                    row = {"mac_user": mac_res, "username": username, "domain": dom_res}
                    data.append(row)
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_USERNAME}' bad formatted, row [{i}]\n"
                    )
        return data

    def open_rssi(self):
        """
        open_rssi
        ---------
        The method opens the file containing the rssi value
        of the connection of the user.
        ### Output:
            - List of dictionaries with the data
        """
        data = []
        with open(FILE_RSSI, "r") as file_object:
            for i, line in enumerate(file_object):
                try:
                    mac_res = parse.search(f"iso.{OID_RSSI}.{{}} =", line)
                    mac_res = self.convert_hex_notation(mac_res[0])
                    rssi_res = parse.search("INTEGER: {:d}", line)[0]
                    row = {
                        "mac_user": mac_res,
                        "rssi": rssi_res,
                    }
                    data.append(row)
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_RSSI}' bad formatted, row [{i}]\n"
                    )
        return data

    def open_snr(self):
        """
        open_snr
        --------
        The method opens the file containing the snr value of
        the connection of the user.
        ### Output:
            - List of dictionaries with the data
        """
        data = []
        with open(FILE_SNR, "r") as file_object:
            for i, line in enumerate(file_object):
                try:
                    mac_res = parse.search(f"iso.{OID_SNR}.{{}} =", line)
                    mac_res = self.convert_hex_notation(mac_res[0])
                    snr_res = parse.search("INTEGER: {:d}", line)[0]
                    row = {
                        "mac_user": mac_res,
                        "snr": snr_res,
                    }
                    data.append(row)
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_SNR}' bad formatted, row [{i}]\n"
                    )
        return data

    def open_bytes_rx(self):
        """
        open_bytes_rx
        -------------
        The method opens the file containing the received
        bytes in the connection of the user.
        ### Output:
            - List of dictionaries with the data
        """
        data = []
        with open(FILE_BYTES_RX, "r") as file_object:
            for i, line in enumerate(file_object):
                try:
                    mac_res = parse.search(f"iso.{OID_BYTES_RX}.{{}} =", line)
                    mac_res = self.convert_hex_notation(mac_res[0])
                    bytes_rx = parse.search("Counter64: {:d}", line)[0]
                    row = {
                        "mac_user": mac_res,
                        "byte_rx": bytes_rx,
                    }
                    data.append(row)
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_BYTES_RX}' bad formatted, row [{i}]\n"
                    )
        return data

    def open_bytes_tx(self):
        """
        open_bytes_tx
        -------------
        The method opens the file containing the transmitted
        bytes in the connection of the user.
        ### Output:
            - List of dictionaries with the data
        """
        data = []
        with open(FILE_BYTES_TX, "r") as file_object:
            for i, line in enumerate(file_object):
                try:
                    mac_res = parse.search(f"iso.{OID_BYTES_TX}.{{}} =", line)
                    mac_res = self.convert_hex_notation(mac_res[0])
                    bytes_tx = parse.search("Counter64: {:d}", line)
                    row = {
                        "mac_user": mac_res,
                        "byte_tx": bytes_tx[0],
                    }
                    data.append(row)
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_BYTES_TX}' bad formatted, row [{i}]\n"
                    )
        return data

    def open_client_type(self):
        """
        open_client_type
        --------------
        Method to retrieve the type of client
        """
        data = []
        with open(FILE_CLIENT_TYPE, "r") as file_object:
            for i, line in enumerate(file_object):
                try:
                    mac_res = parse.search(f"iso.{OID_BYTES_RX}.{{}} =", line)
                    mac_res = self.convert_hex_notation(mac_res[0])
                    bytes_rx = parse.search("INTEGER: {:d}", line)[0]
                    row = {
                        "mac_user": mac_res,
                        "client_type": bytes_rx,
                    }
                    data.append(row)
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_CLIENT_TYPE}' bad formatted, row [{i}]\n"
                    )
        return data

    def open_ap_mac(self):
        """
        open_ap_mac
        -----------
        The method opens the file containing the base radio
        mac of the connection of the user.
        ### Output:
            - List of dictionaries with the data
        """
        data = []
        regex = r"[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}"
        with open(FILE_AP_MAC, "r") as file_object:
            for i, line in enumerate(file_object):
                try:
                    mac_res = parse.search(f"iso.{OID_AP_MAC}.{{}} =", line)
                    mac_res = self.convert_hex_notation(mac_res[0])
                    ap_mac = re.findall(regex, line)[0]
                    ap_mac = ap_mac.replace(" ", ":").lower()
                    ap_name = self.assign_ap_name(ap_mac)
                    row = {
                        "mac_user": mac_res,
                        "name_ap": ap_name,
                    }
                    data.append(row)
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_AP_MAC}' bad formatted, row [{i}]\n"
                    )
        return data

    def open_ap_web(self):
        """
        open_ap_web
        -----------
        The method opens the file containing code of the AP
        inside the SNMP tree and its MAC address .
        ### Output:
            - List of dictionaries with the data
        """
        data = []
        regex = r"[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}\s[0-9A-Fa-f]{2}"
        with open(FILE_AP_WEB, "r") as file_object:
            for i, line in enumerate(file_object):
                try:
                    code_res = parse.search(f"iso.{OID_AP_WEB}.{{}} Hex", line)
                    code_res = code_res[0][:-4]
                    ap_mac = re.findall(regex, line)[0]
                    ap_mac = ap_mac.replace(" ", ":").lower()
                    row = {
                        "code_ap": code_res,
                        "mac_ap": ap_mac,
                    }
                    data.append(row)
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_AP_WEB}' bad formatted, row [{i}]\n"
                    )
        return data

    def open_ap_name(self):
        """
        open_ap_name
        ------------
        The method opens the file containing the name of the
        access points.
        ### Output:
            - List of dictionaries with the data
        """
        data = []
        regex = re.compile(r"AP[A-Za-z0-9\-]{1,20}")
        with open(FILE_AP_NAME, "r") as file_object:
            for i, line in enumerate(file_object):
                try:
                    code_res = parse.search(f"iso.{OID_AP_NAME}.{{}} =", line)
                    ap_name = regex.findall(line)
                    row = {
                        "code_ap": code_res[0],
                        "name_ap": ap_name[0],
                    }
                    data.append(row)
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_AP_NAME}' bad formatted, row [{i}]\n"
                    )
        return data

    def open_primary_channels(self):
        """
        open_primary_channels
        -------------
        Read the primary channels of the AP and returns it in a
        list of dictionaries
        """
        data = []
        with open(FILE_PRIMARY_CH, "r") as file_object:
            i = 0
            for line in file_object:
                try:
                    ap_res = parse.search(f"iso.{OID_PRIMARY_CH}.{{}} =", line)
                    code_ap = ap_res[0][:-2]
                    channel1 = parse.search("INTEGER: {:d}", line)[0]
                    new_line = next(file_object)
                    ap_res = parse.search(f"iso.{OID_PRIMARY_CH}.{{}} =", new_line)
                    assert ap_res[0][:-2] == code_ap
                    channel2 = parse.search("INTEGER: {:d}", new_line)[0]

                    row = {
                        "code_ap": code_ap,
                        "channel_1": channel1,
                        "channel_2": channel2,
                    }
                    data.append(row)
                    i += 1
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_PRIMARY_CH}' bad formatted, row [{i}]\n"
                    )
        return data

    def open_channel_utilization(self):
        """
        open_channel_utilization
        --------------
        Read the channel utilization and returns it in a
        list of dictionaries
        """
        data = []
        with open(FILE_CHANNEL_UTIL, "r") as file_object:
            i = 0
            for line in file_object:
                try:
                    ap_res = parse.search(f"iso.{OID_CHANNEL_UTIL}.{{}} =", line)
                    code_ap = ap_res[0][:-2]
                    channel1 = parse.search("INTEGER: {:d}", line)[0]
                    new_line = next(file_object)
                    ap_res = parse.search(
                        f"iso.{OID_CHANNEL_UTIL}.{{}} =",
                        new_line,
                    )
                    assert ap_res[0][:-2] == code_ap
                    channel2 = parse.search("INTEGER: {:d}", new_line)[0]

                    row = {
                        "code_ap": code_ap,
                        "ch_utilization_1": channel1,
                        "ch_utilization_2": channel2,
                    }
                    data.append(row)
                    i += 1
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_CHANNEL_UTIL}' bad formatted, row [{i}]\n"
                    )
        return data

    def open_noise(self):
        """
        open_noise
        --------
        The method opens the file containing the noise value of
        all the channel for every AP
        ### Output:
            - List of dictionaries with the data
        """
        data = []
        with open(FILE_NOISE, "r") as file_object:
            for i, line in enumerate(file_object):
                try:
                    mac_res = parse.search(f"iso.{OID_NOISE}.{{}} =", line)
                    list1 = mac_res[0].split(".")
                    mac_res = [x for i, x in enumerate(list1) if i < 6]
                    ch_res = [x for i, x in enumerate(list1) if i >= 6]
                    mac_res = reduce(lambda x, y: x + "." + y, mac_res)
                    mac_res = self.convert_hex_notation(mac_res)
                    noise_res = parse.search("INTEGER: {:d}", line)[0]
                    if ch_res[0] == 0:
                        row = {
                            "code_ap": mac_res,
                            "channel_1": ch_res[1],
                            "channel_2": None,
                            "noise": noise_res,
                        }
                    elif ch_res[0] == 1:
                        row = {
                            "code_ap": mac_res,
                            "channel_1": None,
                            "channel_2": ch_res[1],
                            "noise": noise_res,
                        }
                    data.append(row)
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_NOISE}' bad formatted, row [{i}]\n"
                    )
        return data

    def open_tx_power(self):
        """
        open_tx_power
        --------------
        Read the channel transmitted power and returns it in a
        list of dictionaries
        """
        data = []
        with open(FILE_POWER_TX, "r") as file_object:
            i = 0
            for line in file_object:
                try:
                    ap_res = parse.search(f"iso.{OID_POWER_TX}.{{}} =", line)
                    code_ap = ap_res[0][:-2]
                    channel1 = parse.search("INTEGER: {:d}", line)[0]
                    new_line = next(file_object)
                    ap_res = parse.search(f"iso.{OID_POWER_TX}.{{}} =", new_line)
                    assert ap_res[0][:-2] == code_ap
                    channel2 = parse.search("INTEGER: {:d}", new_line)[0]

                    row = {
                        "code_ap": code_ap,
                        "tx_power_1": channel1,
                        "tx_power_2": channel2,
                    }
                    data.append(row)
                    i += 1
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_POWER_TX}' bad formatted, row [{i}]\n"
                    )
        return data

    def open_client_on_channel(self):
        """
        open_client_on_channel
        --------------
        Read the channel connected clients and returns it in a
        list of dictionaries
        """
        data = []
        with open(FILE_N_CLIENT, "r") as file_object:
            i = 0
            for line in file_object:
                try:
                    ap_res = parse.search(f"iso.{OID_N_CLIENT}.{{}} =", line)
                    code_ap = ap_res[0][:-2]
                    channel1 = parse.search("Counter32: {:d}", line)[0]
                    new_line = next(file_object)
                    ap_res = parse.search(f"iso.{OID_N_CLIENT}.{{}} =", new_line)
                    assert ap_res[0][:-2] == code_ap
                    channel2 = parse.search("Counter32: {:d}", new_line)[0]

                    row = {
                        "code_ap": code_ap,
                        "ch_clients_1": channel1,
                        "ch_clients_2": channel2,
                    }
                    data.append(row)
                    i += 1
                except:
                    self.error.write(
                        f"Error in {self.myself} - file: '{FILE_N_CLIENT}' bad formatted, row [{i}]\n"
                    )
        return data

    def convert_hex_notation(self, mac_string):
        """
        convert_hex_notation
        --------------------
        The method converts the mac address from format
        '\d.\d.\d.\d.\d.\d' to '([0-9a-f]:){5}[0-9a-f]' in
        hexadecimal
        ### Input:
            - the MAC string formatted
        ### Output:
            - MAC address formatted
        """
        list_num = mac_string.split(".")
        for i in range(len(list_num)):
            list_num[i] = hex(int(list_num[i]))
        extended_mac = ":".join(list_num)
        return extended_mac.replace("0x", "")

    def merge_dataframes(self):
        """
        merge_dataframes
        ----------------
        The method merges the all dataframes in only one
        ### Output:
            - the dataframe containing the all data
        """
        result = pd.merge(self.df_usernames, self.rssi, on="mac_user")
        result = pd.merge(result, self.snr, on="mac_user", how="right")
        result = pd.merge(result, self.byte_rx, on="mac_user", how="right")
        result = pd.merge(result, self.byte_tx, on="mac_user", how="right")
        result = pd.merge(result, self.client_type, on="mac_user", how="right")
        return pd.merge(result, self.ap_mac, on="mac_user")

    def assign_class(self, domain_list):
        """
        assign_class
        ------------
        The method gives a class to each user based on the
        domain
        ### Input:
            - the list of domains
        ### Output:
            - the list of classes assigned
        """
        classes = []
        for domain in domain_list:
            if domain != domain:
                classes.append("Unknown")
            elif domain == "studenti.polito.it":
                classes.append("Student")
            elif domain == "polito.it":
                classes.append("Staff")
            elif domain == "polito.guest":
                classes.append("Guest")
            else:
                classes.append("External")
        return classes

    def assign_ap_name(self, code):
        """
        assign_ap_name
        --------------
        Given the code of the access point the
        method returns its name.
        ### Input:
            - the code of the AP
        ### Output:
            - the name of the AP
        """
        return self.dict_ap_aggregate.get(code)
