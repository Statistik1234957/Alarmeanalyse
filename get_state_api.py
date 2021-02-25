from config_utils import ConfigUtils
import requests
import pandas as pd
import json
import function_collector
import time

def get_state_api(starttime,endtime,bearer_token,machineid,data_name):

    " This function contains the api connection "

    # api needs iso time formatted string
    starttime_iso = starttime.isoformat() + ".000Z"
    endtime_iso = endtime.isoformat() + ".000Z"

    #get constants from config file
    cfg = ConfigUtils()
    qarc_url = cfg.read_cfgvalue("API","qarc")

    #authentification
    payload = {}
    headers = {
        'x-grob-jwt': bearer_token,
        'Authorization': 'Bearer ' + bearer_token
    }

    if data_name == "isanyaxismoving":

        url = qarc_url + "/analyze/2.0.0/" + "productionStates" + "/byMachineAndPeriod?id=" + machineid + "&from=" + starttime_iso + "&until=" + endtime_iso

    elif data_name == "isdisturbed":

        url = "https://qarc.cloud4machine.com/analyze/2.0.0/productionStates/byMachineAndPeriod?id=20001228&from=2020-11-10T22:00:00.000Z&until=2020-11-25T11:00:00.000Z"

    elif data_name == "mode":

        url = qarc_url + "/s/analyze/1.0.0/machines/" + "spindle" + "/aggregate?id=" + machineid + "&from=" + starttime_iso + "&until=" + endtime_iso

    url = "https://qarc.cloud4machine.com/analyze/2.0.0/productionStates/byMachineAndPeriod?id=20001228&from=2020-11-10T22:00:00.000Z&until=2020-11-25T11:00:00.000Z"

    start_sec = 2
    punishment = 4
    limit = 16

    while 1:
        try:

            if start_sec == limit:
                start_sec = (limit - 1)

            # get the the responses
            response = requests.request("GET", url, headers=headers, data=payload)
            data = response.text
            json_string = json.loads(data)

        except Exception:
            print(f"There has been an error getting Information from the api: Waiting {punishment * start_sec} seconds and trying again.")
            time.sleep(punishment*start_sec)
            start_sec += 1
            continue
        break

    try:

        df = pd.json_normalize(json_string["searchResults"])

        #correct the time
        function_collector.api_time_correction(df)

    except Exception:

        df = pd.DataFrame(columns=["machineid","timestamp","isanyaxismoving","isdisturbed","mode"])

    return df

