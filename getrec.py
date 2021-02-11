import pandas as pd
import os
import glob
import function_collector
from config_utils import ConfigUtils

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_recdata(path):

    d = {}
    df = pd.DataFrame()

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
        df = df.append(d[filename])


    # sort the df, ascending: Oldest value at the top
    df = df.sort_values(by="Alarm-Startzeitpunkt")

    # convert to iso format
    function_collector.format_Alamr_zeit_toiso(df)
    df = df.drop(["y", "x"], axis=1)

    # reset the index of the df
    df.reset_index(inplace=True, drop=True)

    # drop duplicate rows from df
    df.drop_duplicates(inplace=True)

    return df

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_rec2(machine):

    # gets the paths from the Files from the config file
    cfg = ConfigUtils()
    first_path = cfg.read_cfgvalue("Drec", "alarmerec")

    #creates the full path
    fullpath = first_path + machine

    # gets the data from the path
    df = get_recdata(fullpath)

    # adds the machineid col to the dataframe
    m_list = machine.split("\G", 1)[1]
    m_names = "G" + m_list
    df["machineid"] = m_names

    return df


def getrec_total(machinelist):

    dict_rec = {}
    df = pd.DataFrame()

    #combines data of all machine id's
    for i in range(len(machinelist)):
        dict_rec[i] = get_rec2(machinelist[i])
        df = df.append(dict_rec[i])

    #get rid of crazy data
    df["Alarm-ID"] = pd.to_numeric(df["Alarm-ID"],errors= "coerce")
    df = df.dropna(subset=["Alarm-ID"])
    df = df.dropna(subset=["Alarm-Startzeitpunkt"])

    df = df[df["Alarm-ID"].notna()]
    df = df[df["Alarm-Startzeitpunkt"].notna()]

    #sort values
    df = df.sort_values(by="Alarm-Startzeitpunkt", ascending=True)

    return df




