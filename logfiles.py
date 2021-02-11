import pandas as pd
import os
import glob
import numpy as np
from config_utils import ConfigUtils

def getstoplog():

    #create empty dictionary and DataFrame
    d = {}
    df = pd.DataFrame()

    #get path from config file
    cfg = ConfigUtils()
    stoplog_path = cfg.read_cfgvalue("Dlog", "stoplog")

    # collect files with important phrases
    for filename in glob.glob(os.path.join(stoplog_path, "*.log")):
        infile = filename

        important = []
        keep_phrases = ["Logging signal triggert", "Global operation mode"]

        with open(infile) as f:
            f = f.readlines()

        for line in f:
            for phrase in keep_phrases:
                if phrase in line:
                    important.append(line)
                    break

        d[filename] = pd.DataFrame()
        address = ["Date", "NC"]
        d[filename]["Address"] = address
        d[filename]["Index"] = [important[0], important[1]]
        d[filename] = d[filename].transpose()
        d[filename] = d[filename].drop(["Address"])
        d[filename] = d[filename].rename(columns={0: "Stoplog", 1: "NCK-Data"})

        df = df.append(d[filename])

        df[["Stoplogtime", "stoplog"]] = df["Stoplog"].str.extract(
            r"(.{19})(.*)", expand=True
        )

        df[["NCK-Data", "x"]] = df["NCK-Data"].str.split(r"\n", expand=True)
        df = df.drop(["x"], axis=1)

    try:
        df = df.drop(["Stoplog"], axis=1)
        df = df.drop(["stoplog"], axis=1)

        return df

    except KeyError:

        print("The given Dataframe is empty. Please check your Path")

        return None

def getstoplogalarms():

    # create empty dictionary and DataFrame
    d = {}
    df = pd.DataFrame()

    # get path from config file
    cfg = ConfigUtils()
    stoplog_path = cfg.read_cfgvalue("Dlog", "stoplog")

    # collect files with dynamic count of Alarms
    for filename in glob.glob(os.path.join(stoplog_path, "*.log")):

        with open(filename) as f:
            data = f.readlines()[2:14]

        d[filename] = pd.DataFrame()

        d[filename] = pd.DataFrame(data[3:14], columns=["Alarme"])
        d[filename].loc[:,"Stoplog"] = pd.Series(data[0])
        d[filename].loc[d[filename]["Alarme"].str.contains("Tool"), "Alarme"] = np.nan

        d[filename] = d[filename].dropna(thresh=1)
        d[filename] = d[filename][d[filename]["Alarme"] != "\n"]
        d[filename]["Stoplog"] = d[filename]["Stoplog"].ffill()
        d[filename] = d[filename].drop_duplicates()

        df = df.append(d[filename])

    try:
        df[["Stoplogtime", "stoplog"]] = df["Stoplog"].str.split("\t", 1, expand=True)
        df[["Alarmtime", "Alarmid", "Message"]] = df["Alarme"].str.split(
            "\t", 2, expand=True
        )

        df["Nachricht"] = df["Message"].str.split("\n", 1, expand=False)

        df["Nachricht"] = df["Nachricht"].map(lambda x: x[:-1])

        df = df.drop(["stoplog", "Stoplog"], axis=1)
        df = df.drop(["Alarme"], axis=1)
        df = df.drop(["Message"], axis=1)

        return df

    except KeyError:

        print("The given Dataframe is empty. Please check your Path")

        return None

def getstoplog_total():

    #merge both Dataframes by stoplogtime (already in ISO format)
    stoplog_withnc = getstoplog()
    stoplog_w_alarms = getstoplogalarms()
    total_stoplog = stoplog_withnc.merge(stoplog_w_alarms, how= "inner", on =["Stoplogtime"])
    total_stoplog.to_csv("Stoplogtotal", index=False)

    return total_stoplog

