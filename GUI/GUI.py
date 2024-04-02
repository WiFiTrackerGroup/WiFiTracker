from pymongo import MongoClient
import streamlit as st
import folium
from folium.plugins import HeatMap
from datetime import datetime
from config import *
from PIL import Image
import pandas as pd
import seaborn as sns
import matplotlib.pyplot  as plt
import pickle
import io
import os
import numpy as np
from mongoDB_library import *
import DummyTestForHeatMap
from shapely.geometry import Point, Polygon

PATHS = ROOMS
CLIENT = MongoClient(URL_DB)
MYDB = CLIENT[DBNAME]
MYCOUNT = mongo_library(MYDB[COUNTNAME], COUNTNAME)
TEST = DummyTestForHeatMap.TEST

def contactMongo(room, current, date, time):

    timestamp2 = datetime.combine(date, time)
    timestamp1 = timestamp1 - datetime.timedelta(minutes=10)
    if current:
        df = MYCOUNT.findLastBy_room(room)
    else:
        df = MYCOUNT.findBy_class_period(room, timestamp1, timestamp2)

    return df.loc[0, 'N_people']

def contactMongoDummy(room, current, date, time):
    return TEST[room]

def selection(rooms):

    # Title for Menu
    st.sidebar.title("Settings")

    # Select Action
    act = ["--select--", "Room occupancy", "Flows"]
    action = st.sidebar.selectbox("Select action", act)

    # Possible room choice and selection
    if action == "Room occupancy":
        rooms.insert(0, "--select--")
        choice = st.sidebar.selectbox("Select a room", rooms)
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
            time = st.sidebar.time_input("Select time")

    return action, choice, current, date, time

def visualization(choice, date, time):

    # Format
    date = date.strftime("%d %B %Y, %A")
    time = time.strftime("%I:%M")

    # Visualization
    st.write(f"<strong>Selected room:</strong> {choice}", unsafe_allow_html=True)
    st.write(f"<strong>Selected date and time:</strong> {date} {time}", unsafe_allow_html=True)

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
        occupancy[i] = contactMongoDummy(room_list[i], current, date, time)
    return occupancy
    
def visualizeTable(choice, current, date, time):

    # Check if the choice has been made
    if not choice in PATHS:
        return
    
    room_list = list(PATHS[choice]["room_list"].keys())

    occupancy = getOccupancy(room_list, current, date, time)
    data = {'Room': room_list,
            'Occupancy': occupancy}
    df = pd.DataFrame(data)
    st.table(df)

    return df

def int_coord(poly):
    minx, miny, maxx, maxy = map(int, poly.bounds)
    points = [(x,y) for x in range(minx, maxx+1) for y in range(miny, maxy+1) if Point(x,y).within(poly)]
    return points
            
def visualizeMap(choice, df):

    # Check if the choice has been made
    if not choice in PATHS:
        return
    
    # Select path
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, PATHS[choice]["image_path"])

    # Get room list and dictionary containing for each room the coordinates of the boundaries
    room_list = list(PATHS[choice]["room_list"].keys())
    room_dict = PATHS[choice]["room_list"]

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
    rooms = list(PATHS.keys())

    # take the choice of the user and visualize it
    action, choice, current, date, time = selection(rooms)
    # visualization(choice, date, time)

    # Wrong date and time warning
    if not check(date, time):
        st.write('<span style="color:red">Data not available!</span>', unsafe_allow_html=True)
        st.write('<span style="color:red">Please inserta a valid date!</span>', unsafe_allow_html=True)
    else:

        if action == "Room occupancy":
            # Visualize data and map about the choesn room
            df = visualizeTable(choice, current, date, time)
            visualizeMap(choice, df)
        elif action == "Flows":
            st.write("Arriving soon")

if __name__ == "__main__":
    main()