from pymongo import MongoClient
import streamlit as st
import folium
from folium.plugins import HeatMap
from datetime import datetime, timedelta
from sub.config import *
from sub.config_gui import *
from sub.utils import *
from PIL import Image
import pandas as pd
import ast
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pickle
import io
import os
import numpy as np
from sub.mongoDB_library import *

# from tracking import *
# from DummyTestForHeatMap import *
from shapely.geometry import Point, Polygon

CLIENT = MongoClient(URL_DB)
MYDB = CLIENT[DBNAME]
MYCOUNT = mongo_library(MYDB[COUNTNAME], COUNTNAME)
MYTRACKING = mongo_library(MYDB[TRACKNAME], TRACKNAME)
MYINPUT = mongo_library(MYDB[INPUTNAME], INPUTNAME)

TIME = "Room Occupancy Time Series"
FLOW = "Distribution Flows"
HEAT = "Room Occupancy Heat Map"
INPUT = "Rooms True Value"


def getForHeatMap(room, current, timestamp):
    if current:
        df = MYCOUNT.findBy_room_timestamp(room, datetime.now())
    else:
        df = MYCOUNT.findBy_room_timestamp(room, timestamp)
    try:
        return df.loc[0, "N_people"]
    except:
        return 0


def getTimeSeries(choice, date):
    selected_date = datetime.combine(date, datetime.min.time())

    timestamp1 = selected_date.replace(hour=0, minute=0)
    timestamp2 = selected_date.replace(hour=23, minute=59)

    try:
        df_tracking = MYCOUNT.findBy_room_period(choice, timestamp1, timestamp2)
        df_tracking = update_MongoDB_df(df_tracking, choice, timestamp1, timestamp2)
    except Exception as e:
        display_Mongo_not_responding()
        return None
    return df_tracking


def getOccupancy(room_list, current, timestamp):
    occupancy = np.zeros(len(room_list)).tolist()
    try:
        for i in range(len(occupancy)):
            # occupancy[i] = TEST_HEAT[room_list[i]]
            occupancy[i] = getForHeatMap(room_list[i], current, timestamp)
    except Exception as e:
        display_Mongo_not_responding()
        return None
    return occupancy


def getOD(current, timestamp):
    try:
        if current == True:
            df_tracking = MYTRACKING.findTimestamp_forTracking(timestamp)
        else:
            df_tracking = MYTRACKING.findTimestamp_forTracking(timestamp)
    except Exception as e:
        display_Mongo_not_responding()
        return None
    return df_tracking


def visualizeTS(choice, current, date):

    err = ["", "--select--"]
    if choice in err:
        return

    # path = os.path.dirname(os.path.abspath(__file__))
    # path = os.path.join(path, "Dummy_time_series.csv")
    # df = pd.read_csv(path)
    # df = df.loc[df["Room"] == choice]

    df = getTimeSeries(choice, date)

    if df is None:
        return
    elif df.empty:
        display_no_data()
        return

    df = df.drop("Room", axis=1)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    if current:
        st.empty()
        df = df.sort_values(by="Timestamp", ascending=False)
        occupancy = df.iloc[0]["N_people"]
        st.markdown(
            f"<h5>Current number of people in the room: {occupancy}</h5>",
            unsafe_allow_html=True,
        )

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    st.line_chart(df, x="Timestamp", y="N_people")


def visualizeHM(choice, current, timestamp):

    # Check if the choice has been made
    if not choice in ROOMS:
        return

    room_list = list(ROOMS[choice]["room_list"].keys())

    occupancy = getOccupancy(room_list, current, timestamp)

    if occupancy is None:
        return
    elif len(occupancy) == 0:
        display_no_data()
        return

    data = {"Room": room_list, "Occupancy": occupancy}
    df = pd.DataFrame(data)
    df["Occupancy"] = df["Occupancy"].astype(int)
    st.table(df)

    visualizeMap(choice, df)

    return


def display_Mongo_not_responding():
    container = st.empty()

    # Add styled text to the container
    container.markdown(
        "<div style = 'padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #32CD32;'>"
        "<h3 style='color: #32CD32;'>Sorry, the database is not responding</h3>"
        "<h4 style='font-style: italic;'>🍃Try again in some minutes🍃</p>"
        "</div>",
        unsafe_allow_html=True,
    )


def display_no_data():
    container = st.empty()

    # Add styled text to the container
    container.markdown(
        "<div style = 'padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #0066ff;'>"
        "<h3 style='color: #0066ff;'>Sorry, no data found for the considered time period</h3>"
        "<h4 style='font-style: italic;'>🚀Please, try inserting a new period🚀</p>"
        "</div>",
        unsafe_allow_html=True,
    )


def visualizeOD(current, timestamp):

    od_csv = getOD(current, timestamp)

    if od_csv is None:
        display_no_data()
        return
    elif od_csv.empty:
        display_no_data()
        return

    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "then.csv")
    # od_csv = pd.read_csv(path)
    # od_csv['To'] = od_csv['To'].apply(ast.literal_eval)
    timetracking = od_csv["Timestamp"].iloc[0]
    rooms = list(ROOM_LIST.keys())
    list_of_rooms = list()
    groups = dict()
    for r in rooms:
        list_of_rooms.extend(list(ROOM_LIST[r]["room_list"]))
        groups[r] = list(ROOM_LIST[r]["room_list"])

    list_of_rooms = list(set(list_of_rooms))

    dati = np.zeros([len(list_of_rooms), len(list_of_rooms)])
    df = pd.DataFrame(dati, index=list_of_rooms, columns=list_of_rooms)
    time_track = set_tracking_labels(int(timestamp.hour))
    for index, row in od_csv.iterrows():
        origin = row["From"]
        if origin in list_of_rooms:
            destination_list = row["To"]
            for j in destination_list:
                destination = j[0]
                if destination in list_of_rooms:
                    value = j[1]
                    df.loc[origin, destination] = value

    od = pd.DataFrame(index=groups.keys(), columns=groups.keys(), dtype=int)

    for o_zone, o_rooms in groups.items():
        for d_zone, d_rooms in groups.items():
            od.loc[o_zone, d_zone] = df.loc[o_rooms, d_rooms].sum().sum()

    od = od.astype(int)
    label = list()
    colors = list()

    for r in rooms:
        label.append(ROOM_LIST[r]["name"])
        colors.append(ROOM_LIST[r]["color"])
    for r in rooms:
        label.append(ROOM_LIST[r]["name"])
        colors.append(ROOM_LIST[r]["color"])

    source = list()
    target = list()
    value = list()

    for i in range(len(rooms)):
        for j in range(len(rooms)):
            source.append(i)
            target.append(j + len(rooms))
            value.append(od.loc[rooms[i], rooms[j]])

    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=label,
                    color=colors,
                ),
                link=dict(source=source, target=target, value=value),
            )
        ]
    )
    fig.update_layout(
        title_text=f"Movement of people between timeslots: {time_track[0]} ⇔ {time_track[1]}",
        title_font=dict(size=20),
    )
    st.plotly_chart(fig)


def visualizeMap(choice, df):

    # Check if the choice has been made
    if not choice in ROOMS:
        return

    # Select path
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "sub/Image", ROOMS[choice]["image_path"])

    # Get room list and dictionary containing for each room the coordinates of the boundaries
    room_list = list(ROOMS[choice]["room_list"].keys())
    room_dict = ROOMS[choice]["room_list"]

    # Convert image to PNG and visualize
    image_bmp = Image.open(path)
    max_x, max_y = image_bmp.size
    image_png = Image.new("RGBA", image_bmp.size, (255, 255, 255, 255))
    image_png.paste(image_bmp.convert("RGBA"), (0, 0), image_bmp.convert("RGBA"))

    heatmap_data = np.zeros((max_y + 1, max_x + 1))
    file_name = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(file_name, "sub/Image", choice + ".pkl")
    with open(file_name, "rb") as file:
        coord = pickle.load(file)

    for n in range(len(room_list)):
        val = int(df.at[n, "Occupancy"])
        current = coord[room_list[n]]
        for el in current:
            heatmap_data[el[1], el[0]] = val

    fig, ax = plt.subplots()
    h = ax.imshow(
        np.asarray(image_png), extent=[0, image_bmp.width, 0, image_bmp.height]
    )
    h = ax.imshow(
        pd.DataFrame(heatmap_data),
        cmap="inferno",
        alpha=0.5,
        extent=[0, image_bmp.width, 0, image_bmp.height],
    )
    cbar = plt.colorbar(h, shrink=0.5, orientation="horizontal")
    ax.axis("off")
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    st.image(buffer, use_column_width=True)


def addData(timestamp):
    interim = list()
    groups = list(ROOM_LIST.keys())
    for group in groups:
        interim.extend(ROOM_LIST[group]["room_list"])
    interim.insert(0, "--select--")
    choice = st.selectbox("Select a room", interim)

    value = st.text_input("Number of people in the room:")

    if st.button("Send"):

        if not value.isdigit():

            container = st.empty()
            container.markdown(
                "<div style = 'padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #ff5733;'>"
                "<h3 style='color: #ff5733;'>The number of people in a room should be an integer number!</h3>"
                "<h4 style='font-style: italic;'>🚨Please insert the right value!🚨</p>"
                "</div>",
                unsafe_allow_html=True,
            )

            return

        if choice == "--select--":

            container = st.empty()
            container.markdown(
                "<div style = 'padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #ff5733;'>"
                "<h3 style='color: #ff5733;'>To add the data, also the room to which the data refers must be selected!</h3>"
                "<h4 style='font-style: italic;'>🚨Please select a room!🚨</p>"
                "</div>",
                unsafe_allow_html=True,
            )

            return

        value = int(value)

        dict = {"N_people": [value], "Room": [choice], "Timestamp": [timestamp]}

        if not MYINPUT.insert_true_value(dict):
            display_Mongo_not_responding()
            return

        container = st.empty()
        container.markdown(
            "<div style = 'padding: 20px; border-radius: 10px; text-align: center; border: 2px solid ##00ff00;'>"
            "<h3 style='color: #00ff00;'>Data has been succesfully added!</h3>"
            "<h4 style='font-style: italic;'>🌟 Thank you! 🌟</p>"
            "</div>",
            unsafe_allow_html=True,
        )


def check(date, time):

    # Current
    date_now = datetime.now(pytz.timezone("Europe/Rome")).date()
    time_now = datetime.now(pytz.timezone("Europe/Rome")).time()

    # Check that the date is
    if date_now < date:
        return False
    elif date_now == date:
        if time_now < time:
            return False
        else:
            return True
    else:
        return True


def showInstruction(action):
    c_notes = st.empty()
    if action == TIME:
        st.markdown(
            "<style>.styled {list-style: none; padding-left: 0; margin: 0;li {margin-bottom: 10px;display: flex;;align-items: flex-start; \
                    &::before {\
                    content: '✅'; margin-right: 10px;}\
                    &:nth-child(2)::before {\
                    content: '🕒';}\
                    &:nth-child(3)::before {\
                    content: '🗓️';}\
                    &:nth-child(4)::before {\
                    content: '👆🏻';}}}<style>",
            unsafe_allow_html=True,
        )
        c_notes.markdown(
            "<p style='font-size: 20px;'> Here it is possible to see the number of people inside a room during a day at intervals of 15 minutes.\
                <br>To a better experience on the website keep in mind that:</p>"
            "<ul class='styled'>\
                 <li style='font-size: 20px;'>By using the selector on the left side of the panel, it is possible to define the room and day to inspect.</li>\
                 <li style='font-size: 20px;'>If the \"See previous data\" function is not used, the data related to the current day are shown.</li>\
                 <li style='font-size: 20px;'>By using the \"See previous data\" function and selecting a date in the dashboard, the data for the selecetd date are obtained</li>\
                 <li style='font-size: 20px;'>Passing the mouse on the time series, the number of people at each acquisition slot will be displayed.</li>\
             </ul>",
            unsafe_allow_html=True,
        )
    elif action == HEAT:
        st.markdown(
            "<style>.styled {list-style: none; padding-left: 0; margin: 0;li {margin-bottom: 10px;display: flex;;align-items: flex-start; \
                    &::before {\
                    content: '✅'; margin-right: 10px;}\
                    &:nth-child(2)::before {\
                    content: '⏳';}\
                    &:nth-child(3)::before {\
                    content: '🔄';}}}<style>",
            unsafe_allow_html=True,
        )
        c_notes.markdown(
            "<p style='font-size: 20px;'>For some blocks of rooms, a heatmap can be visualized\
                <br>To a better experience on the website keep in mind that:</p>"
            "<ul class='styled'>\
                 <li style='font-size: 20px;'>By using the selector on the left side of the panel, it is possible to select the block of rooms to inspect.</li>\
                 <li style='font-size: 20px;'>Old data can be shown using the \"See previous data\" function and selecting the desired date and time.</li>\
                 <li style='font-size: 20px;'>The room occupancy changes every 15 minutes.</li>\
             </ul>",
            unsafe_allow_html=True,
        )
    elif action == FLOW:
        st.markdown(
            "<style>.styled {list-style: none; padding-left: 0; margin: 0;li {margin-bottom: 10px;display: flex;;align-items: flex-start; \
                    &::before {\
                    content: '✅'; margin-right: 10px;}\
                    &:nth-child(2)::before {\
                    content: '⏳';}\
                    &:nth-child(3)::before {\
                    content: '👆🏻';}}}<style>",
            unsafe_allow_html=True,
        )
        c_notes.markdown(
            "<p style='font-size: 20px;'>Here it is possible to see a representation of the flow of the people moving within the major area of PoliTo.\
                The evaluation of the flow is done every 1 hour and a half to better see the travel of the students during the time change.<br>\
                To a better experience on the website keep in mind that:</p>"
            "<ul class='styled'>\
                 <li style='font-size: 20px;'>By using the selector on the left side of the panel, it is possible to define the timeslot to show.</li>\
                 <li style='font-size: 20px;'>Old data can be shown using the \"See previous data\" function and selecting the desired date and time.</li>\
                 <li style='font-size: 20px;'>Passing the mouse over the colored part of the room and over the flows in grey, you can see the number of people starting and flowing in the other section of PoliTo.</li>\
             </ul>",
            unsafe_allow_html=True,
        )
    elif action == INPUT:
        st.markdown(
            "<style>.styled {list-style: none; padding-left: 0; margin: 0;li {margin-bottom: 10px;display: flex;;align-items: flex-start; \
                    &::before {\
                    content: '✌️'; margin-right: 10px;}\
                    &:nth-child(2)::before {\
                    content: '🎯';}\
                    &:nth-child(3)::before {\
                    content: '⚠️';}}<style>",
            unsafe_allow_html=True,
        )
        c_notes.markdown(
            "<p style='font-size: 20px;'>Insert true number of people in your room, this will help us in increase the performance of our algorithm.\
            <br>Beware, follow the subsequent safety guidelines:</p>"
            "<ul class='styled'>\
             <li style='font-size: 20px;'>Count at least two times the number of people in the room.</li>\
                 <li style='font-size: 20px;'>Insert a precise number and not one only 'near' the true number of people.</li>\
                 <li style='font-size: 20px;'>Double check the name of room in which you are.</li>\
             </ul>"
            "<p style='font-size: 20px;'>Otherwise you will create a False value in our ground truth.</p>",
            unsafe_allow_html=True,
        )
    else:
        c_notes.markdown(
            "<p style='font-size: 20px;'>   Hello there! 👋<br>   We are a group of ICT4SS students from the Politecnico di Torino! <br>The interface is easy to use, just select the desired data in the menu on the left and enjoy the search!</p>",
            unsafe_allow_html=True,
        )


def selection():

    # Title for Menu
    st.sidebar.title("Settings")

    # Select Action
    act = ["--select--", TIME, FLOW, HEAT, INPUT]
    action = st.sidebar.selectbox("Select action", act)

    # Time selection
    current = True
    date = datetime.now(pytz.timezone("Europe/Rome")).date()
    time = datetime.now().time()
    time2 = datetime.now()
    if is_legal_time():
        time2 += timedelta(hours=2)
    else:
        time2 += timedelta(hours=1)
    current_time = datetime.strptime("10:00", "%H:%M")
    dates = []
    for _ in range(8):
        dates.append(datetime.combine(date, current_time.time()))
        current_time += timedelta(minutes=90)

    for i in range(1,len(dates)+1):
        if time2 > dates[-i]:
            time = dates[-i].time()
            break
    if action != "--select--":
        showInstruction(action)

    if action != "--select--" and action != INPUT:
        current = st.sidebar.checkbox("See previous data")
        current = not current
        if not current:
            # To select date and time
            date = st.sidebar.date_input("Select date")
            if action != TIME:
                if action==HEAT:
                    time = st.sidebar.time_input("Select time")
                if action==FLOW: 
                    start = datetime.combine(datetime.today(), datetime.min.time()).replace(hour=10, minute=0)
                    t = []
                    delta = 90
                    n = 8
                    for i in range(int(n)):
                        t.append(start.time().strftime('%H:%M'))
                        start += timedelta(minutes=delta)
                    t.insert(0, "--select--")
                    time = st.sidebar.selectbox("Select timeslot", t)
                    if time != "--select--":
                        time = datetime.strptime(time, "%H:%M").time()
                        # Possible room choice and selection
    if action == HEAT:
        rooms = list(ROOMS.keys())
        rooms_name = list()
        revert = dict()
        for r in rooms:
            rooms_name.append(ROOMS[r]["name"])
            revert[ROOMS[r]["name"]] = r
        rooms_name.insert(0, "--select--")
        revert["--select--"] = ""
        choice = st.sidebar.selectbox("Select a room", rooms_name)
        choice = revert[choice]
    elif action == TIME:
        interim = list()
        groups = list(ROOM_LIST.keys())
        for group in groups:
            interim.extend(ROOM_LIST[group]["room_list"])
        interim.insert(0, "--select--")
        choice = st.sidebar.selectbox("Select a room", interim)
    else:
        choice = ""

    return action, choice, current, date, time


def main():

    # Start the application and give a title
    st.title("🛜 Wi-Fi Tracker")
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #333;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # take the choice of the user and visualize it
    action, choice, current, date, time = selection()
    # visualization(choice, date, time)
    c_notes = st.empty()
    if action == "--select--":
        c_notes.markdown(
            "<p style='font-size: 20px;'>   Hello there! 👋<br>   We are a group of ICT4SS students from the Politecnico di Torino! <br>The interface is easy to use, just select the desired data in the menu on the left and enjoy the search!</p>",
            unsafe_allow_html=True,
        )
    else:
        c_notes.empty()
    # Wrong date and time warning
    if time == "--select--":
        pass
    elif not check(date, time):
        container = st.empty()

        # Add styled text to the container
        container.markdown(
            "<div style = 'padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #ff5733;'>"
            "<h3 style='color: #ff5733;'>Sorry, the application is not able to predict the future!</h3>"
            "<h4 style='font-style: italic;'>🚨Please insert a valid date!🚨</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        timestamp = datetime.combine(date, time)
        if is_legal_time():
            timestamp -= timedelta(hours=2)
        else:
            timestamp -= timedelta(hours=1)
        if action == HEAT:
            visualizeHM(choice, current, timestamp)
        elif action == FLOW:
            visualizeOD(current, timestamp)
        elif action == TIME:
            visualizeTS(choice, current, date)
        elif action == INPUT:
            addData(timestamp)


if __name__ == "__main__":
    main()
