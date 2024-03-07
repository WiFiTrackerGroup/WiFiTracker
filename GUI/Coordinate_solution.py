import cv2
import matplotlib.pyplot as plt
import os 
import config

PATHS = config.rooms

# Load image 
choice = "R First Floor"
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, PATHS[choice]["image_path"])
image = cv2.imread(path)
print(path)

# Click event
def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        print(f"Coordinate del punto cliccato - X: {event.xdata}, Y: {event.ydata}")

# Visualize image
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title(choice)
plt.connect('button_press_event', onclick)
plt.show()