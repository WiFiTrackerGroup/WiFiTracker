import pandas as pd
from .config import *
import pickle


class Counting_P:
    def __init__(self):
        model_path = "Service/sub/ml_models/random_forest.sav"
        self.rndForest_regr = pickle.load(open(model_path, "rb"))

    def room_division(self, dataRoom):
        """
        room_division
        -------------
        take all the data and divide the rooms of all PoliTo
        ### Output:
            - the dataframe with the room divided
        """
        Ap = "AP-AULA"
        dataRoom = dataRoom[dataRoom["name_ap"].notnull()]
        dataRoom = dataRoom[dataRoom["name_ap"].str.contains(Ap)]
        rooms = pd.DataFrame()
        max_l = max([len(sublist.split("-")) for sublist in dataRoom["name_ap"]])
        if max_l == 2:
            rooms[["AP", "Room"]] = dataRoom["name_ap"].str.split("-", expand=True)
        elif max_l == 3:
            rooms[["AP", "Room", "APnum"]] = dataRoom["name_ap"].str.split(
                "-", expand=True
            )
        elif max_l == 4:
            rooms[["AP", "Room", "APnum", "NaN"]] = dataRoom["name_ap"].str.split(
                "-", expand=True
            )
        elif max_l == 5:
            rooms[["AP", "Room", "APnum", "NaN", "other"]] = dataRoom[
                "name_ap"
            ].str.split("-", expand=True)
        else:
            raise Exception("Error in dataRoom['name_ap'].str.split('-', expand=True)")

        dataRoom = pd.concat([dataRoom, rooms], axis=1)
        dataRoom = dataRoom.drop(["AP", "NaN"], axis=1)
        return dataRoom

    def baseline(self, dataRoom):
        timestamp = dataRoom["Timestamp"].iloc[0]
        dataRoom = (
            dataRoom.drop_duplicates("user_masked")
            .groupby(["Room", "class"])["AP"]
            .count()
        )
        dataRoom = dataRoom.unstack(level="class")
        dataRoom.fillna(0, inplace=True)
        dataRoom["N_people"] = dataRoom.sum(axis="columns", numeric_only=True)
        dataRoom = dataRoom.reset_index()
        dataRoom["Timestamp"] = timestamp
        return dataRoom

    def feature_extraction(self, dataRoom: pd.DataFrame):
        feature_dict = {
            "room": [],
            "n_devices": [],
            "n_users": [],
            "snr_mean": [],
            "snr_std": [],
            "rssi_mean": [],
            "rssi_std": [],
            "ch_util_2_4_mean": [],
            "ch_util_5_mean": [],
            "noise_2_4_mean": [],
            "noise_5_mean": [],
            "n_people": [],
        }
        rooms = dataRoom["Room"].unique()
        for room in rooms:
            df_room = dataRoom[dataRoom["Room"] == room]
            feature_dict["room"].append(room)

            # Feature extrapolation
            df_dist_ap = df_room.drop_duplicates(subset="APnum")
            n_devices = (
                df_dist_ap["n_clients_2_4"].sum() + df_dist_ap["n_clients_5"].sum()
            )
            feature_dict["n_devices"].append(n_devices)

            df_dist_users = df_room.drop_duplicates(subset="user_masked")
            n_users = len(df_dist_users[df_dist_users["snr"] > 20])
            feature_dict["n_users"].append(n_users)

            snr_mean = df_room["snr"].mean()
            feature_dict["snr_mean"].append(snr_mean)
            snr_std = df_room["snr"].std()
            feature_dict["snr_std"].append(snr_std)

            rssi_mean = df_room["rssi"].mean()
            feature_dict["rssi_mean"].append(rssi_mean)
            rssi_std = df_room["rssi"].std()
            feature_dict["rssi_std"].append(rssi_std)

            ch_util_2_4_mean = df_dist_ap["ch_utilization_2_4"].mean()
            feature_dict["ch_util_2_4_mean"].append(ch_util_2_4_mean)
            ch_util_5_mean = df_dist_ap["ch_utilization_5"].mean()
            feature_dict["ch_util_5_mean"].append(ch_util_5_mean)

            noise_2_4_mean = df_dist_ap["noise_2_4"].mean()
            feature_dict["noise_2_4_mean"].append(noise_2_4_mean)
            noise_5_mean = df_dist_ap["noise_5"].mean()
            feature_dict["noise_5_mean"].append(noise_5_mean)

        df_features = pd.DataFrame.from_dict(feature_dict)
        return df_features

    def random_forest_regr(self, dataRoom: pd.DataFrame):
        timestamp = dataRoom["Timestamp"].iloc[0]
        # EXtract features
        df_features = self.feature_extraction(dataRoom)
        X = df_features.loc[:, df_features.columns != "room"].to_numpy()
        y = self.rndForest_regr.predict(X)
        df_features["N_people"] = y
        dataRoom = dataRoom.join(df_features[["room", "N_people"]], on="Room")
        dataRoom = dataRoom.reset_index()
        dataRoom["Timestamp"] = timestamp
        return dataRoom

    def feature_extraction(self, dataRoom: pd.DataFrame):
        feature_dict = {
            "room": [],
            "n_devices": [],
            "n_users": [],
            "snr_mean": [],
            "snr_std": [],
            "rssi_mean": [],
            "rssi_std": [],
            "ch_util_2_4_mean": [],
            "ch_util_5_mean": [],
            "noise_2_4_mean": [],
            "noise_5_mean": [],
            "n_people": [],
        }
        rooms = dataRoom["Room"].unique()
        for room in rooms:
            df_room = dataRoom[dataRoom["Room"] == room]
            feature_dict["room"].append(room)

            # Feature extrapolation
            df_dist_ap = df_room.drop_duplicates(subset="APnum")
            n_devices = (
                df_dist_ap["n_clients_2_4"].sum() + df_dist_ap["n_clients_5"].sum()
            )
            feature_dict["n_devices"].append(n_devices)

            df_dist_users = df_room.drop_duplicates(subset="user_masked")
            n_users = len(df_dist_users[df_dist_users["snr"] > 20])
            feature_dict["n_users"].append(n_users)

            snr_mean = df_room["snr"].mean()
            feature_dict["snr_mean"].append(snr_mean)
            snr_std = df_room["snr"].std()
            feature_dict["snr_std"].append(snr_std)

            rssi_mean = df_room["rssi"].mean()
            feature_dict["rssi_mean"].append(rssi_mean)
            rssi_std = df_room["rssi"].std()
            feature_dict["rssi_std"].append(rssi_std)

            ch_util_2_4_mean = df_dist_ap["ch_utilization_2_4"].mean()
            feature_dict["ch_util_2_4_mean"].append(ch_util_2_4_mean)
            ch_util_5_mean = df_dist_ap["ch_utilization_5"].mean()
            feature_dict["ch_util_5_mean"].append(ch_util_5_mean)

            noise_2_4_mean = df_dist_ap["noise_2_4"].mean()
            feature_dict["noise_2_4_mean"].append(noise_2_4_mean)
            noise_5_mean = df_dist_ap["noise_5"].mean()
            feature_dict["noise_5_mean"].append(noise_5_mean)

        df_features = pd.DataFrame.from_dict(feature_dict)
        return df_features

    def random_forest_regr(self, dataRoom: pd.DataFrame):
        timestamp = dataRoom["Timestamp"].iloc[0]
        # EXtract features
        df_features = self.feature_extraction(dataRoom)
        X = df_features.loc[:, df_features.columns != "room"].to_numpy()
        y = self.rndForest_regr.predict(X)
        df_features["N_people"] = y
        dataRoom = dataRoom.join(df_features[["room", "N_people"]], on="Room")
        dataRoom = dataRoom.reset_index()
        dataRoom["Timestamp"] = timestamp
        return dataRoom

    def filter(self, dataRoom):
        # Remove devices that may be connected from different rooms
        dataRoom = dataRoom[dataRoom["snr"] > 20]
        # Remove devices that are categorized as sensors
        dataRoom = dataRoom[dataRoom["class"] != "Unknown"]
        return dataRoom

    def main(self, dataRoom):
        dataRoom = self.room_division(dataRoom)
        dataRoom = self.filter(dataRoom)
        dataRoom = self.random_forest_regr(dataRoom)
        return dataRoom
