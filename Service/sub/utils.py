import pandas as pd
from .config import *
from datetime import datetime, timedelta
import pytz


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
        rooms = rooms.drop(["NaN"], axis=1)
    elif max_l == 5:
        rooms[["AP", "Room", "APnum", "NaN", "other"]] = dataRoom["name_ap"].str.split(
            "-", expand=True
        )
        rooms = rooms.drop(["NaN", "other"])
    else:
        raise Exception("Error in dataRoom['name_ap'].str.split('-', expand=True)")

    dataRoom = pd.concat([dataRoom, rooms], axis=1)
    dataRoom = dataRoom.drop(["AP"], axis=1)
    return dataRoom


def update_MongoDB_df(df, init_timestamp, final_timestamp, room):
    """
    The method checks the timestamps inside the df, starting from the init_timestamp
    up to final_timestamp. If there is a hole between two timestamps a raw with
    0 is inserted.
    Input:
        - df
        - init_timestamp
        - final_timestamp
    Output:
        - df_updated
    """
    list_updated = []
    dict_list = df.to_dict("records")
    current_time = init_timestamp
    i = 0
    while (final_timestamp - current_time).total_seconds() > SCHEDULE:
        if current_time + timedelta(seconds=SCHEDULE) > datetime.now():
            break
        if (
            i == len(dict_list)
            or (df["Timestamp"].iloc[i] - current_time).total_seconds() > 2 * SCHEDULE
        ):
            list_updated.append(
                {"Room": room, "Timestamp": current_time, "N_people": 0}
            )
        else:
            list_updated.append(dict_list[i])
            i += 1
        current_time += timedelta(seconds=SCHEDULE)
    df_updated = pd.DataFrame(list_updated)
    current_timezone = pytz.timezone("Europe/Rome")
    df_updated["Timestamp"] = [
        current_timezone.localize(df_updated["Timestamp"].iloc[i])
        for i in range(len(df_updated["Timestamp"]))
    ]
    return df_updated
