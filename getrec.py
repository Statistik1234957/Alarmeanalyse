import pandas as pd
import os
import glob
import function_collector
from config_utils import ConfigUtils

def get_rec_from_file(path):

    "This Function import the rec_data from a given path"

    # create an empty dict and DF
    d = {}
    df = pd.DataFrame()

    try:
        # import each file and combine them to a  dataframe
        for filename in glob.glob(os.path.join(path, "*.rec.csv")):
            d[filename] = pd.read_csv(
                filename,
                sep=";",
                names=[
                    "Alarm-ID",
                    "Meldung",
                    "Quelle",
                    "Alarm-Startzeitpunkt",
                    "Alarm-Endzeitpunkt",
                ],
            )
            # append to the DF combining all the Data
            df = df.append(d[filename])

    except Exception as e:
        print(e)
        df = pd.DataFrame(columns=["Alarm-ID","Meldung","Quelle","Alarm-Startzeitpunkt","Alarm-Endzeitpunkt"])

    # get the columns with datetime information
    time_collist = ["Alarm-Startzeitpunkt","Alarm-Endzeitpunkt"]

    # convert to iso format
    df = function_collector.format_timestamp_toiso(df,time_collist,format= ' %d.%m.%Y %H:%M:%S',
                                              stringsplit=True)

    return df


def get_rec_per_machine(machine):

    "This Function gets you all the rec files for one specific machine"

    # gets the paths from the Files from the config file
    cfg = ConfigUtils()
    first_path = cfg.read_cfgvalue("Drec", "alarmerec")

    #creates the full path
    fullpath = first_path + machine

    # gets the data from the path
    df = get_rec_from_file(fullpath)

    # adds the machineid col to the dataframe
    df["machineid"] = machine

    return df


def getrec_total(machinelist):

    "This Function gets you all the rec files for all machines"

    # create an empty dict and DF to store the Data
    dict_rec = {}
    df = pd.DataFrame()

    #combines data of all machine id's
    for i in range(len(machinelist)):

        #get the rec data for one machine
        dict_rec[i] = get_rec_per_machine(machinelist[i])

        # append the DF to the DF combining all the Data
        df = df.append(dict_rec[i])

    #only want numeric alarm Ids: NA if fails
    df["Alarm-ID"] = pd.to_numeric(df["Alarm-ID"],errors= "coerce")

    #cols for removing na values
    collist = ["Alarm-ID","Alarm-Startzeitpunkt"]

    # clean the data for saving
    df = function_collector.data_cleaning(df,collist,"Alarm-Startzeitpunkt")

    return df





