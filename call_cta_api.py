#! /usr/bin/env python3
import pandas as pd
import numpy as np
import os
import re
import datetime
import requests
import json
import urllib3
import urllib.request,urllib.parse,urllib.error
from apscheduler.schedulers.background import BlockingScheduler

key_path=os.getcwd()
with open("cta_key.json","r") as cta_key_file:
    json_key_cta=json.load(cta_key_file)
    cta_key=json_key_cta['key1']


def create_url():
    cta_base_url="http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?"
    route_colors=["Red","Blue","Brn",'G',"Org","Pink"]
    route_color=np.random.choice(route_colors)
    print(f"The route used in the API is {route_color}")
    params2={'key':str(cta_key),'rt':route_color,"outputType":"JSON"}
    cta_api_url=str(cta_base_url)+urllib.parse.urlencode(params2)
    return cta_api_url

def extract_cta_data(cta_json_data):
    list_of_fields=["rn","destSt","destNm","trDr","nextStaId"
                    ,"nextStpId","nextStaNm","prdt","arrT","isApp","isDly","lat","lon"]
    if cta_json_data['ctatt']['errCd']=="0":
        cta_timestamp=cta_json_data['ctatt']['tmst']
        cta_routes=cta_json_data['ctatt']['route']
        cta_route_name=cta_routes[0]['@name']
        cta_train=cta_routes[0]['train']
        cta_train_len=len(cta_train)
        cta_df1=pd.DataFrame(np.random.rand(cta_train_len,len(list_of_fields)),columns=list_of_fields)
        cta_df1["ROUTE_NAME"]=cta_route_name
        cta_df1["TIMESTAMP"]=cta_timestamp
        for idx1 in range(cta_train_len):
            for idx2,field in enumerate(list_of_fields):
                cta_df1.iloc[idx1,idx2]=cta_train[idx1][field]
        cta_df1.rename(columns={"rn":"RUN_NUMBER",
                               "destSt":"DEST_STREET",
                               "destNm":"DEST_NAME",
                               "trDr":"TRAIN_ROUTE_NBR",
                               "nextStaId":"NEXT_STATION_ID",
                               "nextStpId":"NEXT_STOP_ID",
                               "nextStaNm":"NEXT_STATION_NAME",
                               "prdt":"PREDICTION_TS",
                               "arrT":"ARRIVAL_TS",
                               "isApp":"IS_APPROACHING",
                               "isDly":"IS_DELAYED",
                                "lat":"LATITUDE",
                                "lon":"LONGITUDE"
                               },inplace=True)
        for col in cta_df1.columns:
            cta_df1[col]=cta_df1[col].apply(str.strip)
            cta_df1[col]=cta_df1[col].apply(str.upper)
            return cta_df1
    else:
        print(f"Error Occurred: {cta_json_data['ctatt']['errNm']}")
        return None

def call_api():
    cta_api_url=create_url()
    try:
        cta_url_response=urllib.request.urlopen(cta_api_url)
    except urllib.error.HTTPError as error1:
        print(f"Sorry could not retrieve the details of the movie {movie_name}")
    except urllib.error.URLError as error2:
        print("Failed to reach the server")
        print(f"Reason: {error2.reason}" )
    else:
        cta_url_data=cta_url_response.read()
        cta_json_data=json.loads(cta_url_data)
        cta_df1=extract_cta_data(cta_json_data)
        cta_df2=cta_df1[["ROUTE_NAME","RUN_NUMBER","DEST_STREET","DEST_NAME","NEXT_STATION_ID"
                     ,"NEXT_STATION_NAME","PREDICTION_TS","ARRIVAL_TS","IS_DELAYED",
                    "LATITUDE","LONGITUDE"]]
        csv_dump_path=key_path+"/cta_api_dump.csv"
        cta_df2.to_csv(csv_dump_path,mode="a",index=False,header=False)
        current_time = datetime.datetime.now()
        print(f"Successfully appended the output at {current_time}")

import time
while True:
    # Code executed here
    time.sleep(10)
    call_api()
