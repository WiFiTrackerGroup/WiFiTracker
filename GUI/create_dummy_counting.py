from config import *
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os


interim = list()
groups = list(ROOM_LIST.keys())
for group in groups:
    interim.extend(ROOM_LIST[group]["room_list"])

today = datetime.now().date()
start_time = datetime(today.year, today.month, today.day, hour=0, minute=0)
end_time = datetime(today.year, today.month, today.day, hour=23, minute=59)  # Esempio: ore 20:00
interval = timedelta(minutes=15)
timestamps = []
current_time = start_time
while current_time <= end_time:
    timestamps.append(current_time)
    current_time += interval

lista1 = list()
lista2 = list()
lista3 = list()

my_list = list()
for t in timestamps:
    for room in interim:
        lista1.append(room)
        lista2.append(t)
        lista3.append(np.random.randint(0,251))
        

df = pd.DataFrame({'Rooms': lista1, 'Timestamp': lista2, 'N_people': lista3})
path = os.getcwd()
file = 'Dummy_time_series.csv'
path = os.path.join(path, file)
df.to_csv(path, index=False)

