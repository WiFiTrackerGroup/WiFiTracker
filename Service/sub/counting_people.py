import pandas as pd
from .config import *


class Counting_P:
    def __init__(self):
        pass

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
        if max_l == 4:
            rooms[["AP", "Room", "APnum", "NaN"]] = dataRoom["name_ap"].str.split(
                "-", expand=True
            )
        elif max_l == 3:
            rooms[["AP", "Room", "APnum"]] = dataRoom["name_ap"].str.split(
                "-", expand=True
            )
        elif max_l == 5:
            rooms[["AP", "Room", "APnum", "NaN", "other"]] = dataRoom[
                "name_ap"
            ].str.split("-", expand=True)
        else:
            raise Exception("Error in dataRoom['name_ap'].str.split('-', expand=True)")

        dataRoom = pd.concat([dataRoom, rooms], axis=1)
        return dataRoom

    def counting_basic(self, dataRoom):
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

    def filter(self, dataRoom):
        # Remove devices that may be connected from different rooms
        dataRoom = dataRoom[dataRoom["snr"] > 20]
        # Remove devices that are categorized as sensors
        dataRoom = dataRoom[dataRoom["class"] != "Unknown"]
        return dataRoom

    def main(self, dataRoom):
        dataRoom = self.room_division(dataRoom)
        dataRoom = self.filter(dataRoom)
        dataRoom = self.counting_basic(dataRoom)
        return dataRoom
