import pandas as pd
import dctreestatus
import function_collector
from datetime import datetime, timedelta
import get_bearer_token
from config_utils import ConfigUtils
import get_state_api

def get_status():

    " This function computes the state Data "

    #get the api constants
    cfg = ConfigUtils()
    email = cfg.read_cfgvalue("API", "email")
    password = cfg.read_cfgvalue("API", "password")
    login_url = cfg.read_cfgvalue("API", "qarclogin")

    # get the bearer token
    bearer_token = get_bearer_token.get_bearer_token(email=email, password=password, loginurl=login_url)

    # set the timespan ################# -> adjust
    endtime = datetime.utcnow().replace(microsecond=0)
    starttime = endtime - timedelta(minutes=360)

    #get the values ################# -> adjust
    #df_mode = get_state_api.get_state_api(starttime,endtime,bearer_token,"G352-2114","mode")
    #df_isdisturbed = get_state_api.get_state_api(starttime,endtime,bearer_token,"G352-2114","isdisturbed")
    #df_anyaxismoving = get_state_api.get_state_api(starttime,endtime,bearer_token,"G352-2114","isanyaxismoving")

#############
    cfg = ConfigUtils()
    mode_path = cfg.read_cfgvalue("Dstate", "datamode")
    disturbed_path = cfg.read_cfgvalue("Dstate", "dataisdisturbed")
    axismoving_path = cfg.read_cfgvalue("Dstate", "dataaxismoving")

    # reads in the Data
    df_mode = pd.read_csv(mode_path, sep=";", header=0, low_memory=False)
    df_isdisturbed = pd.read_csv(disturbed_path, sep=";", header=0, low_memory=False)
    df_anyaxismoving = pd.read_csv(axismoving_path, sep=";", header=0, low_memory=False)

    # Format the Date column
    df_mode[["timestamp", "x"]] = df_mode["timestamp"].str.split(".", expand=True)
    df_isdisturbed[["timestamp", "x"]] = df_isdisturbed["timestamp"].str.split(".", expand=True)
    df_anyaxismoving[["timestamp", "x"]] = df_anyaxismoving["timestamp"].str.split(".", expand=True)

    # Format the Date column
    df_mode[["timestamp", "y"]] = df_mode["timestamp"].str.split("+", expand=True)
    df_isdisturbed[["timestamp", "y"]] = df_isdisturbed["timestamp"].str.split("+", expand=True)
    df_anyaxismoving[["timestamp", "y"]] = df_anyaxismoving["timestamp"].str.split("+", expand=True)

    # drop the rest
    df_mode = df_mode.drop(["x", "y"], axis=1)
    df_isdisturbed = df_isdisturbed.drop(["x", "y"], axis=1)
    df_anyaxismoving = df_anyaxismoving.drop(["x", "y"], axis=1)

###########

    # rename the column for integration
    df_mode = df_mode.rename(columns={"timestamp": "Alarm-Startzeitpunkt"})
    df_isdisturbed = df_isdisturbed.rename(columns={"timestamp": "Alarm-Startzeitpunkt"})
    df_anyaxismoving = df_anyaxismoving.rename(columns={"timestamp": "Alarm-Startzeitpunkt"})

    # get names of the machine ids as list
    midmode = df_mode["machineid"].unique().tolist()
    middis = df_isdisturbed["machineid"].unique().tolist()
    midany = df_anyaxismoving["machineid"].unique().tolist()

    #intersect the lists
    commlist = list(set(midmode).intersection(middis))
    total = list(set(commlist).intersection(midany))

    #create an empty dict and DF
    d = {}
    df = pd.DataFrame()

    #for each machine do:
    for i in range(len(total)):

        #do the calculations
        d[i] = function_collector.get_data_for_calculation(df_mode, df_isdisturbed, df_anyaxismoving, total[i],dataname = "state")

        #get a list of the columns
        collist_fill = d[i].columns

        #fill up those columns
        function_collector.fillup(d[i],collist_fill)

        #apply the Decision Tree
        dctreestatus.dtree(d[i])

        #append the DF to the DF combining all the Data
        df = df.append(d[i])

    #get the columns with datetime information
    time_collist = ["Alarm-Startzeitpunkt"]

    # cols for removing na values
    collist = ["Alarm-Startzeitpunkt","machineid", "Status"]

    #convert to iso format
    df = function_collector.format_timestamp_toiso(df,time_collist,format= "%Y-%m-%d %H:%M:%S",
                                              stringsplit=False)

    # slect only the relevant Data
    df = df[collist]

    #clean the data for saveness
    df = function_collector.data_cleaning(df,collist,"Alarm-Startzeitpunkt")

    return df
