# Useful scripts
The ```ground_truth_eval.sh``` is used to manually collect ground truth values. The others python scripts are used internally by the bash script to perform some operations, so make sure
to put them in the same folder.
## Configuration
Since the python scripts make use of the pandas library install it using ```pip```.
Make sure to set the IP and PORT of the VM running the acquisition module inside the ```ground_truth_eval.sh``` script.
## Usage
Make the script executable and the run it:
```
chmod +x ground_truth_eval.sh
./ground_truth_eval.sh  
```
When running the script requires the name of the room (use the AP controller notation) and the number of people inside the room.
