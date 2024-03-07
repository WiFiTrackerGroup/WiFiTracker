from pymongo import MongoClient
import streamlit as st
import folium
from folium.plugins import HeatMap
from datetime import datetime
from config import *
from PIL import Image
import pandas as pd
import io
import os
import numpy as np
from mongoDB_library import *
import DummyTestForHeatMap

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

    # Possible room choice and selection
    rooms.insert(0, "--select--")
    choice = st.selectbox("Select a room", rooms)

    # Time selection
    current = st.checkbox("See previous data")
    if not current:
        # To use current date and time 
        current = True
        date = datetime.now().date()
        time = datetime.now().time()
    else:
        # To select date and time 
        current= False
        date = st.date_input("Select date")
        time = st.time_input("Select time")

    return choice, current, date, time

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

    x = list()
    y = list()
    for room in room_list:
        x.append(PATHS[choice]["room_list"][room]["X"])
        y.append(PATHS[choice]["room_list"][room]["Y"])
        

    data = {'Room': room_list,
            'Occupancy': occupancy}
    df = pd.DataFrame(data)
    st.table(df)
    data = {'Room': room_list,
            'Occupancy': occupancy,
            'x': x,
            'y': y}
    return pd.DataFrame(data)
    
        
def visualizeMap(choice, df):

    # Check if the choice has been made
    if not choice in PATHS:
        return
    
    # Select path
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, PATHS[choice]["image_path"])

    # Convert image to PNG and visualize
    image_bmp = Image.open(path)
    png_byte_array = io.BytesIO()
    image_bmp.save(png_byte_array, format='PNG')
    st.image(png_byte_array, use_column_width=True)

def main():

    # Sreate the application and give a title
    st.title("Room occupancy visualization")

    # Select available rooms from constants file
    rooms = list(PATHS.keys())

    # take the choice of the user and visualize it
    choice, current, date, time = selection(rooms)
    # visualization(choice, date, time)

    # Wrong date and time warning
    if not check(date, time):
        st.write('<span style="color:red">Data not available!</span>', unsafe_allow_html=True)
        st.write('<span style="color:red">Please inserta a valid date!</span>', unsafe_allow_html=True)
    else:
        # Visualize data and map about the choesn room
        df = visualizeTable(choice, current, date, time)
        visualizeMap(choice, df)

if __name__ == "__main__":
    main()