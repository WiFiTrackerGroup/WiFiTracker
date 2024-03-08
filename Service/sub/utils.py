import pandas as pd


def room_division(dataRoom):
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
    rooms[["AP", "Room", "APnum", "NaN"]] = dataRoom["name_ap"].str.split(
        "-", expand=True
    )
    dataRoom = pd.concat([dataRoom, rooms], axis=1)
    dataRoom = dataRoom.drop(["AP", "NaN"], axis=1)
    return dataRoom
