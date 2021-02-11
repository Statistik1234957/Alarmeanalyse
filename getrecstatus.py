import getstate
import getrec
import pandas as pd
import function_collector

def get_recws(machinelist):

    #imports the status_data
    datastaterel = getstate.get_status()

    #imports the rec_data

    data_rec = getrec.getrec_total(machinelist)

    #machineid of datastaterel
    m_state = datastaterel["machineid"].unique().tolist()

    #machineeid of data_rec
    m_rec = []

    for machine in machinelist:

        m_list = machine.split("\G", 1)[1]
        m_names = "G" + m_list
        m_rec = m_rec + [m_names]

    #get the intersection of both lists
    total_list = list(set(m_state) & set(m_rec))

    # for each machineid and then combine the dataframe
    d = {}
    df = pd.DataFrame()

    for i in range(len(total_list)):

        d[i] = function_collector.datamachineid_rec(datastaterel,data_rec,total_list[i])
        function_collector.fillup_state(d[i])
        df = df.append(d[i])

    # filter out cracy values
    df = df[df["Alarm-Startzeitpunkt"] >= "2019-02-12T07:33:39"]
    df = df[df["Alarm-Startzeitpunkt"] <= "2025-12-10T07:33:44"]

    #filter out statedata and new created row
    df = df[df["Alarm-ID"].notna()]
    df = df[df["Alarm-Startzeitpunkt"].notna()]

    # sort the df, ascending: Oldest value at the top
    df = df.sort_values(by="Alarm-Startzeitpunkt")

    # reset the index of the df
    df.reset_index(inplace=True, drop=True)

    # drop duplicate rows from df
    df.drop_duplicates(inplace=True)

    return df




