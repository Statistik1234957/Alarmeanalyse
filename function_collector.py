import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def api_time_correction(df):

    "This file converts the times given by the api"

    #list with the columns of the df
    collist = df.columns.tolist()

    #list with time columns
    collist_time = ["startTime", "endTime"]

    for col in collist_time:

        if col in collist:

            #microseconds and thus dividision by 1000 needed
            df[col] = df[col].map(lambda x: datetime.utcfromtimestamp(x / 1000))

            #adjust the time format
            df[col] = df[col].map(lambda x: x.replace(microsecond=0))
            df[col] = pd.to_datetime(df[col], errors="coerce", format="%Y-%m-%d %H:%M:%S")

    return df

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_data_for_calculation(df1, df2, df3, machineid,dataname):

    " This Function subsets the relevant data and appends a default row"

    #selects the data at the given machineid (for each Dataframe)
    dfa = df1[df1["machineid"] == machineid]
    dfb = df2[df2["machineid"] == machineid]
    dfc = df3[df3["machineid"] == machineid]

    # append all df's together
    df = dfa.append([dfb, dfc])

    if dataname == "state":
        # adds a new row at the top
        new_row = {
            "machineid": machineid,
            "Alarm-Startzeitpunkt": "1900-07-25 00:00:00",
            "mode": "Automatic",
            "isdisturbed": False,
            "isanyaxismoving": False,
        }
    else:
        new_row = {
            "Alarm-ID": np.NaN,
            "Meldung": "start",
            "Quelle": "start",
            "Alarm-Startzeitpunkt": "1900-07-25T00:00:00",
            "Alarm-Endzeitpunkt": "1900-07-25T00:00:01",
            "machineid": machineid,
            "Status": "No_Status_Data",
        }

    #append the new row to the df
    df = df.append(new_row, ignore_index=True)

    # sort the df, ascending: Oldest value at the top
    df = df.sort_values(by="Alarm-Startzeitpunkt", ascending=True)

    return df

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def fillup(df,collist):

    "This function fills up the missing values in the DF"

    #fill up the missing values and always pick the cell above
    for col in collist:
        df[col].fillna(method="ffill", inplace=True)

    return None

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def format_timestamp_toiso(df,time_collist,format,stringsplit):

    "This function transforms the timestamp of the status Data to iso format"

    for col in time_collist:

        if stringsplit == True:

            df[[col, "x"]] = df[col].str.extract(r"(.{20})(.*)", expand=True)
            df.drop("x",axis = 1,inplace = True)

        else:
            None

        # convert the column to datetime object, if fails: NA
        df[col] = pd.to_datetime(df[col], errors="coerce",format=format)

        # convert to isoformat
        df[col] = df[col].map(lambda x: x.isoformat())

    return df

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def data_cleaning(df,collist,sortcolname):

    "This Function removes duplicates and sets a new index"

    #drop empty columns
    df.dropna(subset=collist, inplace=True,axis = 0)

    # sort the df, ascending: Oldest value at the top
    df = df.sort_values(by=sortcolname)

    #remove NaT values from the primary Time column
    df = df[df[sortcolname].notnull()]
    df = df[~df[sortcolname].str.contains('NaT')]

    # reset the index of the df
    df.reset_index(inplace=True, drop=True)

    #get the mean date
    critical_value = df[sortcolname][len(df[sortcolname]) // 2]

    critical_value1 = datetime.strptime(critical_value,'%Y-%m-%dT%H:%M:%S') - timedelta(days=360)
    critical_value1 = critical_value1.strftime('%Y-%m-%dT%H:%M:%S')

    critical_value2 = datetime.strptime(critical_value, '%Y-%m-%dT%H:%M:%S') + timedelta(days=360)
    critical_value2 = critical_value2.strftime('%Y-%m-%dT%H:%M:%S')

    # filter out cracy values
    df = df[df[sortcolname] >= critical_value1]
    df = df[df[sortcolname] <= critical_value2]

    # reset the index of the df
    df.reset_index(inplace=True, drop=True)

    # drop duplicate rows from df
    df.drop_duplicates(inplace=True)

    return df

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #








