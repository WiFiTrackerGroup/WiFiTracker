# SNMP REST Interface
The first step of the WiFi-Tracker application starts with the acquisition module, which is responsible for the collection of all the raw data from the AP. This module can be contacted only via an authorized IP through a REST interface because it will manage private data. To be GDPR compliant indeed this data has to be anonymized.

Moreover, the Politecnico network is composed of more than 900 access points located in all its different venues, and to manage it all a controller is needed. The work of this first module is in fact to communicate with the AP controller to acquire all the different data, aggregate it, anonymize the critical information, and then send it to the next module.

## Configuration
First of all, if the machine that will run the code does note have installed the snmp module run:
```
sudo apt-get install snmp
```
Then create a virtual environment and install the packages with:
```
pip install -r requirements.txt
```

Moreover, the code of the SNMP_REST folder can run only on a VM connected to the Politecnico network.
To configure the server properly make sure to change the **COMMUNITY** and **IP_WLC** field in the *config.py* file.

Once this is done the server is ready to use.

## Usage
### Running the webservice
Make sure to run the code from the *SNMP_REST* folder.
```
cd SNMP_REST
python3 snmp_rest.py
```
As said before if the **COMMUNITY** and **IP_WLC** are not correct the AP controller cannot be contacted and then the application will probably return an empty JSON or an error message.

### Requests from client
#### GET available
- **/AP**:

  contains the information about the AP MAC and its relative name, which will usually consist of the name of the room in which it is positioned.
- **/data**:

  contains all the devices’ needed information, which includes the MAC of the device, the e-mail used for the authentication, the SNR and RSSI of the connection, the amount of data transmitted/received, the type of the client (used to know if the client is connected to the 2.4 or 5 GHz frequency) and the MAC of the AP to which it is connected.
- **/APChannelInfo**:

  consists of all the relevant information about the AP channels, which is additional information that will be next used in the Random Forest Regression to increase the performance of the people-counting segment of the project. The information contained in this case is the MAC of the AP, plus the number of devices connected to each network (2.4 and 5 GHz), the channel used, the noise over the channel, and the percentage of utilization of it(amount of traffic is passing through the channel in %, where 100% is the maximum utilization). This is used to give more features to the ML model for the prediction. The baseline can extrapolate the number of people in the rooms without this data.
- **/test**:

  consist of a test query used to check if the aggregation part of the /data GET is working. Usually it is unused.
