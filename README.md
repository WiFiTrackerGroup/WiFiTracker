# WiFiTracker

![Python Version](https://img.shields.io/badge/python-3.11%20-informational?style=flat&logo=python&logoColor=white)
![GitHub](https://img.shields.io/github/contributors/WiFiTrackerGroup/WiFiTracker?style=flat&logo=github)
![GitHub](https://img.shields.io/github/license/WiFiTrackerGroup/WiFiTracker?style=flat)

<p align="center">
  <img src="https://github.com/BDRVinICT4SS/WiFiTracker/assets/118899936/3c11ef63-5948-4ff1-8ee8-c322b31fc75e" width="400"/>
</p>

# What is WiFi tracker?
WiFiTracker is an application that aims to estimate the number of people inside rooms and track the movements of people between areas exploiting the Wi-Fi infrastucture.
Universities and other public places often offer Wi-Fi access for free by logging in with private credentials, opening the possibility to query the controller of the network to obtain information on the devices connected. However, the number of devices is usually different from the actual number of people inside a building, especially in universities or workplaces where people have more than one device.
The idea of the Wi-FiTracker is to use Machine Learning to estimate the real number of people inside a building.
Since this project started in Politecnico di Torino we used the Wi-Fi architecture present in the campus.
# High-level architecture
![image]()
The application is structured in three different modules:
1. Acquisition module: is responsible to query the Access points (APs) controller through the SNMP protocol and perform data anonymization and preprocessing.
2. Processing module: is where the number of people is estimated using a Random Forest Regression and where the flows of people are calculated.
3. Visualization module: is a web interface, developed using [Streamlit](https://github.com/streamlit/streamlit), to easily visualize the processed data.
