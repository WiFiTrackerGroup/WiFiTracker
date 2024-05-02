#!/bin/bash
IP = ""
PORT = ""
LOGS_PATH = "./logs"
echo -e "\nSet room name:"
read room_name
echo -e "\nSet number of people in $room_name:"
read n_people

date=$(date +%m_%d_%Y_%H_%M_%S)
file_path_user="${LOGS_PATH}/${date}_${room_name}_${n_people}"

echo -e "\nRetrieving data..."
status_code=$(curl "http://${IP}:${PORT}/data" -o "${file_path_user}.json" -w '%{http_code}\n')
if [ "$status_code" = "200" ]; then
	echo -e "\nData retrieved successfully!"
else
	echo -e "\nRequest was not successfull!"
	exit 1
fi

echo -e "\nConverting file to csv..."
python3 to_csv.py "${file_path_user}.json"
if [ $? = 0 ]; then
	echo "Converted successfully!"
	rm "${file_path_user}.json"
else
	echo "Error in converting to csv!"
fi

file_path_ap="${LOGS_PATH}/ap_info_${date}_${room_name}_${n_people}"

echo -e "\nRetrieving AP channel info"
status_code=$(curl "http://${IP}:${PORT}/APChannelInfo" -o "${file_path_ap}.json" -w '%{http_code}\n')
if [ "$status_code" = "200" ]; then
	echo -e "\nAP info retrieved successfully!"
else
	echo -e "\nRequest was not successfull!"
	exit 1
fi

echo -e "\nConverting file to csv..."
python3 to_csv.py "${file_path_ap}.json"
if [ $? = 0 ]; then
	echo "Converted successfully!"
	rm "${file_path_ap}.json"
else
	echo "Error in converting to csv!"
fi

python3 concat_apInfo_user.py "${file_path_user}.csv" "${file_path_ap}.csv"
if [ $? = 0 ]; then
	echo "Concatended successfully!"
	rm "${file_path_ap}.csv"
else
	echo "Error in concateneting"
fi

