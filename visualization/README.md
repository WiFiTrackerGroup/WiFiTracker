# Visualization module
The last step of the WiFi-Tracker application is the visualization. This module is used by the user to visualize the data collected in the previous part in an easy and intuitive way.

This module is responsible of showing the user which types of data are available and, once the user has chosen what they want to see, collect the data from mongoDB.

## Configuration
Make sure to create a python virtual environment and install through ```pip``` the required libraries.
```
pip install -r requirements.txt
```
In the ```config.py``` change the IP and PORT field according to your needs.

## Usage
### Running the webservice
The module can be easily started using the command
```
cd visualization
streamlit run gui.py
```

### General structure

The module is based on a main function. This function manages the visualization of the initial page and calls first to another function which manage the settings menu and then, once the user has chosen the settings, it will pass the corresponding data to one among four function used for four different functionalities supported by the application.

Among the four functionalities, three are used to visualize data (Distribution Flows, Heat Map, and Time Series), and the last is used to add data as ground truth for the prediction model (True Value).

#### Settings

The ```selection``` function is used to generate the settings menu and to get the configuration of them provided by the user. At first the user is required to select which of the four functionalities they want to use. At that point, for each functionalities, different settings can be set:
- **Distribution Flows**:

  Through a button, the user can eanable the selection of the time and date to which the data will refer (otherwise current data will be shown).
- **Heat Map**:

  Through a button, the user can eanable the selection of the time and date to which the data will refer (otherwise current data will be shown). Also, the user can select the data of which zone will be displayed. The different zone are predefined by the map.
- **Time Series**:

  Through a button, the user can eanable the selection of the date to which the data will refer (otherwise data of the current day will be shown). Also the user can select the data of which room will be displayed.
- **True Value**:
  No settings are required for this functionality.