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
    max_l = max([len(sublist.split("-")) for sublist in dataRoom["name_ap"]])
    if max_l == 2:
        rooms[["AP", "Room"]] = dataRoom["name_ap"].str.split("-", expand=True)
    elif max_l == 3:
        rooms[["AP", "Room", "APnum"]] = dataRoom["name_ap"].str.split("-", expand=True)
    elif max_l == 4:
        rooms[["AP", "Room", "APnum", "NaN"]] = dataRoom["name_ap"].str.split(
            "-", expand=True
        )
        dataRoom = dataRoom.drop(["AP", "NaN"], axis=1)
    elif max_l == 5:
        rooms[["AP", "Room", "APnum", "NaN", "other"]] = dataRoom["name_ap"].str.split(
            "-", expand=True
        )
        dataRoom = dataRoom.drop(["other"])
    else:
        raise Exception("Error in dataRoom['name_ap'].str.split('-', expand=True)")

    dataRoom = pd.concat([dataRoom, rooms], axis=1)
    try:
        dataRoom = dataRoom.drop(["NaN"])
    except:
        pass
    dataRoom = dataRoom.drop(["AP"], axis=1)
    return dataRoom
