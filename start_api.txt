
# This script starts the Python script call_cta_api.py
#!/bin/bash
rm cta_api_dump.csv
echo "ROUTE_NAME,RUN_NUMBER,DEST_STREET,DEST_NAME,NEXT_STATION_ID,NEXT_STATION_NAME,PREDICTION_TS,ARRIVAL_TS,IS_DELAYED,LATITUDE,LONGITUDE" > cta_api_dump.csv
python3 call_cta_api.py
exit 0

