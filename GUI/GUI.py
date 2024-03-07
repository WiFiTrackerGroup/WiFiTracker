from pymongo import MongoClient
import streamlit as st
import folium
from folium.plugins import HeatMap
from datetime import datetime
import config
from PIL import Image
import pandas as pd
import io
import os

PATHS = config.image_path

def selection(rooms):

    # Possible room choice and selection
    rooms.insert(0, "--select--")
    choice = st.selectbox("Select a room", rooms)

    # Time selection
    current = st.checkbox("See previous data")
    if not current:
        # To use current date and time 
        date = datetime.now().date()
        time = datetime.now().time()
    else:
        # To select date and time 
        date = st.date_input("Select date")
        time = st.time_input("Select time")

    return choice, date, time

def visualization(choice, date, time):

    # Format
    date = date.strftime("%d %B %Y, %A")
    time = time.strftime("%I:%M")

    # Visualization
    st.write(f"<strong>Selected Room:</strong> {choice}", unsafe_allow_html=True)
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
    
def visualizeTable(choice):

    # Check if the choice has been made
    if not choice in PATHS:
        return

    data = {'Nome': ['Alice', 'Bob', 'Charlie'],
            'Età': [25, 30, 35],
            'Città': ['Roma', 'Milano', 'Firenze']}
    df = pd.DataFrame(data)
    st.table(df)
        
def visualizeMap(choice):

    # Check if the choice has been made
    if not choice in PATHS:
        return
    
    # Select path
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, PATHS[choice])

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
    choice, date, time = selection(rooms)
    visualization(choice, date, time)

    # Wrong date and time warning
    if not check(date, time):
        st.write('<span style="color:red">Data not available!</span>', unsafe_allow_html=True)
        st.write('<span style="color:red">Please inserta a valid date!</span>', unsafe_allow_html=True)
    else:
        # Visualize data and map about the choesn room
        visualizeTable(choice)
        visualizeMap(choice)

if __name__ == "__main__":
    main()