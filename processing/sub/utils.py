import pandas as pd
from .config import *
from datetime import datetime, timedelta
import pytz


def room_division(dataRoom):
    """Divide entries on rooms, not on AP number"""

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


def update_MongoDB_df(df, room, init_timestamp, final_timestamp):
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
            current_time += timedelta(seconds=SCHEDULE)
        else:
            list_updated.append(dict_list[i])
            current_time = df["Timestamp"].iloc[i]
            i += 1
    df_updated = pd.DataFrame(list_updated)
    if is_legal_time():
        shift = 2
    else:
        shift = 1
    df_updated["Timestamp"] = [
        df_updated["Timestamp"].iloc[i] + timedelta(hours=shift)
        for i in range(len(df_updated["Timestamp"]))
    ]
    return df_updated


def is_legal_time():
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)

    local_timezone = pytz.timezone("Europe/Rome")
    local_now = utc_now.astimezone(local_timezone)

    return local_now.dst() != timedelta(0)


def set_tracking_labels(hour):
    dict_labels = {
        7: ("hearly-morning", "8.30 - 10.00"),
        8: ("8.30 - 10.00", "10.00 - 11.30"),
        9: ("8.30 - 10.00", "10.00 - 11.30"),
        10: ("10.00 - 11.30", "11.30 - 13.00"),
        11: ("10.00 - 11.30", "11.30 - 13.00"),
        12: ("11.30 - 13.00", "13.00 - 14.30"),
        13: ("13.00 - 14.30", "14.30 - 16.00"),
        14: ("14.30 - 16.00", "16.00 - 17.30"),
        15: ("14.30 - 16.00", "16.00 - 17.30"),
        16: ("16.00 - 17.30", "17.30 - 19.00"),
        17: ("17.30 - 19.00", "evening"),
    }
    try:
        return dict_labels[hour]
    except:
        return ("Not during lessons", "PoliTO closed")
