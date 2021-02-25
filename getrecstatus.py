import getstate
import getrec
import pandas as pd
import function_collector

def get_recws(machinelist):

    "This function combines the rac Data with the State Data"

    # create an empty dict and DF to store the Data
    d = {}
    df = pd.DataFrame()
    df_empty = pd.DataFrame(columns= ["machineid"])

    # get the rec data
    data_rec = getrec.getrec_total(machinelist)

    #get the state Data
    datastaterel = getstate.get_status()

    for i in range(len(machinelist)):

        # get a list of the columns
        collist_fill = ["Status"]

        # do the calculations
        d[i] = function_collector.get_data_for_calculation(datastaterel, data_rec, df_empty, machinelist[i],
                                                           dataname="rec")

        # fill up those columns
        function_collector.fillup(d[i],collist_fill)

        # append the DF to the DF combining all the Data
        df = df.append(d[i])

    #collist for checking
    collist = ["Status","Alarm-ID","Alarm-Startzeitpunkt"]

    # clean the data for saveness
    df = function_collector.data_cleaning(df,collist,"Alarm-Startzeitpunkt")

    return df




