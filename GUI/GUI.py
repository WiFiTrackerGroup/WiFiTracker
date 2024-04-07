from pymongo import MongoClient
import streamlit as st
import folium
from folium.plugins import HeatMap
from datetime import datetime, timedelta
from config import *
from PIL import Image
import pandas as pd
import ast
import seaborn as sns
import matplotlib.pyplot  as plt
import plotly.graph_objects as go
import pickle
import io
import os
import numpy as np
from mongoDB_library import *
from tracking import *
from DummyTestForHeatMap import *
from shapely.geometry import Point, Polygon

CLIENT = MongoClient(URL_DB)
MYDB = CLIENT[DBNAME]
MYCOUNT = mongo_library(MYDB[COUNTNAME], COUNTNAME)
MYTRACKING = mongo_library(MYDB[TRACKNAME], TRACKNAME)

TIME = "Room Occupancy Time Series"
FLOW = "Distribution Flows"
HEAT = "Room Occupancy Heat Map"


def getForHeatMap(room, current, date, time):

    timestamp2 = datetime.combine(date, time)
    timestamp1 = timestamp2 - timedelta(minutes=15)
    if current:
        df = MYCOUNT.findLastBy_room(room)
    else:
        df = MYCOUNT.findBy_class_period(room, timestamp1, timestamp2)

    return df.loc[0, 'N_people']

def getTimeSeries(choice, date): 
    selected_date = datetime.combine(date, datetime.min.time())

    timestamp1 = selected_date.replace(hour=0, minute=0)
    timestamp2 = selected_date.replace(hour=23, minute=59)

    df_tracking = MYTRACKING.findBy_class_period(choice, timestamp1, timestamp2)
    return df_tracking

def selection():

    # Title for Menu
    st.sidebar.title("Settings")

    # Select Action
    act = ["--select--", TIME, FLOW, HEAT]
    action = st.sidebar.selectbox("Select action", act)

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

    # Time selection
    current = True
    date = datetime.now().date()
    time = datetime.now().time()

    if action != "--select--":
        current = st.sidebar.checkbox("See previous data")
        current = not current
        if not current:
            # To select date and time 
            date = st.sidebar.date_input("Select date")
            if action!=TIME:
                time = st.sidebar.time_input("Select time")

    return action, choice, current, date, time

def timeseries(choice, current, date):

    err = ["", "--select--"]
    if  choice in err:
        return

    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path,"Dummy_time_series.csv")
    df = pd.read_csv(path)
    df = df.loc[df['Room'] == choice]
    #df = getTimeSeries(choice, date)
    df = df.sort_values(by='Timestamp')
    df = df.drop('Room', axis=1)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    st.line_chart(df, x='Timestamp', y='N_people')

def check(date, time):

    # Current
    date_now = datetime.now().date()
    time_now = datetime.now().time()

    # Check that the date is 
    if date_now<date:
        return False
    elif date_now == date:
        if time_now < time:
            return False
        else:
            return True
    else:
        return True
    
def getOccupancy(room_list, current, date, time):
    occupancy = np.zeros(len(room_list)).tolist()
    for i in range(len(occupancy)):
        occupancy[i] = TEST_HEAT[room_list[i]]
        # occupancy[i] = getForHeatMap(room_list[i], current, date, time)
    return occupancy
    
def visualizeTable(choice, current, date, time):

    # Check if the choice has been made
    if not choice in ROOMS:
        return
    
    room_list = list(ROOMS[choice]["room_list"].keys())

    occupancy = getOccupancy(room_list, current, date, time)
    data = {'Room': room_list,
            'Occupancy': occupancy}
    df = pd.DataFrame(data)
    df['Occupancy'] = df['Occupancy'].astype(int)
    st.table(df)

    return df

def getOD(current, date, time):
    if current == True:
        df_tracking = MYTRACKING.findLast_forTracking()
    else:
        timestamp2 = datetime.combine(date, time)
        timestamp1 = timestamp2 - timedelta(minutes=15)
        df_tracking = MYTRACKING.findBy_period(timestamp1, timestamp2)
    return df_tracking

def visualizeOD(current, date, time):

    # od_csv = getOD(current, date, time)
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path,"then.csv")
    od_csv = pd.read_csv(path)
    rooms = list(ROOM_LIST.keys())
    od_csv['To'] = od_csv['To'].apply(ast.literal_eval)

    list_of_rooms = list()
    groups = dict()

    for r in rooms:
        list_of_rooms.extend(list(ROOM_LIST[r]["room_list"]))
        groups[r]=list(ROOM_LIST[r]["room_list"])
    
    list_of_rooms = list(set(list_of_rooms))

    dati =  np.zeros([len(list_of_rooms), len(list_of_rooms)])
    df = pd.DataFrame(dati, index=list_of_rooms, columns=list_of_rooms)

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
            target.append(j+len(rooms))
            value.append(od.loc[rooms[i], rooms[j]])

    


    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = label,
      color = colors
    ),
    link = dict(
      source = source,
      target = target,
      value = value
    ))])

    st.plotly_chart(fig)

def visualizeMap(choice, df):

    # Check if the choice has been made
    if not choice in ROOMS:
        return
    
    # Select path
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path,"Image", ROOMS[choice]["image_path"])

    # Get room list and dictionary containing for each room the coordinates of the boundaries
    room_list = list(ROOMS[choice]["room_list"].keys())
    room_dict = ROOMS[choice]["room_list"]

    # Convert image to PNG and visualize
    image_bmp = Image.open(path)
    max_x, max_y = image_bmp.size
    image_png = Image.new("RGBA", image_bmp.size, (255, 255, 255, 255))
    image_png.paste(image_bmp.convert("RGBA"), (0, 0), image_bmp.convert("RGBA")) 

    heatmap_data = np.zeros((max_y+1, max_x+1))
    file_name = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(file_name, "Image", choice + ".pkl")
    with open(file_name, 'rb') as file:
        coord = pickle.load(file)

    for n in range(len(room_list)):
        val = int(df.at[n, "Occupancy"])
        current = coord[room_list[n]]
        for el in current:
            heatmap_data[el[1], el[0]] = val

    
    fig, ax = plt.subplots()
    h = ax.imshow(np.asarray(image_png), extent=[0, image_bmp.width, 0, image_bmp.height])
    h = ax.imshow(pd.DataFrame(heatmap_data), cmap="inferno", alpha=0.5, extent=[0, image_bmp.width, 0, image_bmp.height])
    cbar = plt.colorbar(h, shrink=0.5, orientation='horizontal')
    ax.axis("off")
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    st.image(buffer,use_column_width=True)

def main():

    # Start the application and give a title
    st.title("Wi-Fi Tracker")
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #333;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Select available rooms from constants file

    # take the choice of the user and visualize it
    action, choice, current, date, time = selection()
    # visualization(choice, date, time)

    # Wrong date and time warning
    if not check(date, time):
        st.write('<span style="color:red">Data not available!</span>', unsafe_allow_html=True)
        st.write('<span style="color:red">Please inserta a valid date!</span>', unsafe_allow_html=True)
    else:

        if action == HEAT:
            # Visualize data and map about the choesn room
            df = visualizeTable(choice, current, date, time)
            visualizeMap(choice, df)
        elif action == FLOW:
            visualizeOD(current, date, time)
        elif action == TIME:
            timeseries(choice, current, date)

if __name__ == "__main__":
    main()
