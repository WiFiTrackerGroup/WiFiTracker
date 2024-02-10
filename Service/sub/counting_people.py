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
        dataRoom = dataRoom[dataRoom["name_ap"].str.contains(Ap)]
        rooms = pd.DataFrame()
        rooms[["AP", "Room", "APnum", "NaN"]] = dataRoom["name_ap"].str.split(
            "-", expand=True
        )
        dataRoom = pd.concat([dataRoom, rooms], axis=1)
        return dataRoom

    def counting_basic(self, dataRoom):
        dataRoom = dataRoom.drop_duplicates("user_masked").groupby("Room").count()
        dataRoom = dataRoom["Timestamp"]
        dataRoom = dataRoom.to_frame()
        dataRoom.rename(columns={"Timestamp": "N_people"}, inplace=True)
        return dataRoom

    def main(self, dataRoom):
        dataRoom = self.room_division(dataRoom)
        dataRoom = self.counting_basic(dataRoom)
