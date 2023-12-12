# SNMP REST Interface
This REST webservice is used to query the AP controller using the SNMP protocol, aggregate the data in a database, and to anonymize MAC address and username of each entry.

## Usage
### Running the webservice
Make sure to run the code from the *SNMP_REST* folder.
```
cd SNMP_REST
python3 snmp_rest.py
```

### Requests from client
#### GET
- **/AP**: aggregate the data related to the access point and return it as JSON file. **NOTE**: It must be run before every other request!
- **/data**: aggregate, anonymize data and return a JSON file.

[comment]: <> (## Data Aquisition)
[comment]: <> (DataAquisition is a class that deals with the acquisition of the data through SNMP query. A series of snmpwalk bash command is used to retrieve the data from the controller of all the acces point of Politecnico. A different set of command can be also used for the acquisition of the information of the acces point, like the mac address connected to it and their names to know their geographical position in the Politecnico.)