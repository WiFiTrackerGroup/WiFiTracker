import cv2
import matplotlib.pyplot as plt
import os 
from config2 import *

PATHS = ROOMS
x = list()
y = list()

# Load image 
choice = "Odd"
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, PATHS[choice]["image_path"])
image = cv2.imread(path)
print(path)

# Click event
def onclick(event):
    global x
    global y
    if event.xdata is not None and event.ydata is not None:
        if len(x)>=4:
            x = list()
            y = list()
        x.append(event.xdata)
        y.append(event.ydata)
        if len(x)==4:
            print(f'"X": {x},\n "Y": {y}')

# Visualize image
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title(choice)
plt.connect('button_press_event', onclick)
plt.show()