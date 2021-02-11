
" this file contains multiple functions used in the code"

import pandas as pd
import numpy as np
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

" 1. Get full dataframe for status_data"

def datamachineid_state(df1, df2, df3, machineid2):

    #Computation of Status by 3 different df's from 3 different files

    #selects the data at the given machineid (for each Dataframe)
    dfa = df1[df1["machineid"] == machineid2]
    dfb = df2[df2["machineid"] == machineid2]
    dfc = df3[df3["machineid"] == machineid2]

    # append all df's together
    df = dfa.append([dfb, dfc])

    # adds a new row at the top
    new_row = {
        "machineid": machineid2,
        "timestamp": "2001-07-25T00:00:00",
        "mode": "Automatic",
        "isdisturbed": False,
        "isanyaxismoving": False,
    }
    #append the new row to the df
    df = df.append(new_row, ignore_index=True)

    # sort the df, ascending: Oldest value at the top -> 2001
    df = df.sort_values(by="timestamp")

    return df

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

" 2. fills up the Dataframe by always picking the cell above for status_data"

def fillup(df):

    #fill up the missing values and always pick the cell above
    df["isanyaxismoving"].fillna(method="ffill", inplace=True)
    df["mode"].fillna(method="ffill", inplace=True)
    df["isdisturbed"].fillna(method="ffill", inplace=True)

    return None

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

" 3. transforms the timestamp of the status Data to iso format"

def fromat_timestamp_toiso(df):

    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce", format = "%Y-%m-%d %H:%M:%S"
    )

    df["timestamp"] = df["timestamp"].map(
        lambda x: x.isoformat()
    )
    return None

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

"1. transform the timestamp  from the Red data"

def format_Alamr_zeit_toiso(df):


    df[["Alarm-Startzeitpunkt", "x"]] = df["Alarm-Startzeitpunkt"].str.extract(
        r"(.{20})(.*)", expand=True
    )
    df['Alarm-Startzeitpunkt'] = pd.to_datetime(df['Alarm-Startzeitpunkt'], errors="coerce",
                                                format=' %d.%m.%Y %H:%M:%S')

    df['Alarm-Startzeitpunkt'] = df['Alarm-Startzeitpunkt'].map(
        lambda x: x.isoformat()
    )

    df[["Alarm-Endzeitpunkt", "y"]] = df["Alarm-Endzeitpunkt"].str.extract(
        r"(.{20})(.*)", expand=True
    )
    df['Alarm-Endzeitpunkt'] = pd.to_datetime(df['Alarm-Endzeitpunkt'], errors="coerce",
                                                format=' %d.%m.%Y %H:%M:%S')

    df['Alarm-Endzeitpunkt'] = df['Alarm-Endzeitpunkt'].map(
        lambda x: x.isoformat()
    )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

"2. combine data_rec and data_state"


def datamachineid_rec(datastaterel, datarec, machineid2):

    df = pd.DataFrame()

    #select statedata for the given machineid
    df_state = datastaterel[datastaterel["machineid"] == machineid2]

    #select recdata for given machineid
    df_rec = datarec[datarec["machineid"] == machineid2]

    # append all df's together
    df = df.append([df_state, df_rec])

    #filter out empty time rows
    df = df.dropna(subset=["Alarm-Startzeitpunkt"])

    new_row = {
        "Alarm-ID": np.NaN,
        "Meldung": "start",
        "Quelle": "start",
        "Alarm-Startzeitpunkt": "1900-07-25T00:00:00",
        "Alarm-Endzeitpunkt": "1900-07-25T00:00:01",
        "machineid": machineid2,
        "Status": "No Status Data",
    }
    # append the new row to the df
    df = df.append(new_row, ignore_index=True)

    # sort the df, ascending: Oldest value at the top -> 1900
    df = df.sort_values(by="Alarm-Startzeitpunkt", ascending=True)

    return df

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

"3. fillup State column"

def fillup_state(df):

    #always fill up with the value above
    df["Status"].fillna(method="ffill", inplace=True)

    return None

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #




