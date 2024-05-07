# Processing module
The processing module is responsible of estimating the number of people inside rooms and to track the movements from and to macro areas inside Politecnico di Torino.
The estimation of the number of people is done using a *Random Forest Regression* algorithm, whose checkpoint is saved in ```processing/sub/ml_models``` folder.

To further train the model you can use the ```rf_regression.ipynb``` notebook inside the ```tools``` folder: remember to save the checkpoint of the model inside the ```ml_models``` folder .

## Configuration
Make sure to create a python virtual environment and install through ```pip``` the required libraries.
```
pip install -r requirements.txt
```
In the ```config.py``` change the IP and PORT field according to your needs.
## Usage
To run the code make sure to be in the *processing* folder.
```
cd processing
python3 processing.py
```
