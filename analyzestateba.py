import pandas as pd
import getrecstatus
import numpy as np


def getstatebeaf(machinelist):

    try:

        df = getrecstatus.get_recws(machinelist)

        m_rec = []

        for machine in machinelist:
            m_list = machine.split("\G", 1)[1]
            m_names = "G" + m_list
            m_rec = m_rec + [m_names]

        dftotal = pd.DataFrame()
        dict = {}

        for k in range(len(m_rec)):

            dict[k] = df[df["machineid"] == m_rec[k]]

            new_row1 = {
                "Alarm-ID": np.NaN,
                "Meldung": "start",
                "Quelle": "start",
                "Alarm-Startzeitpunkt": "1900-07-25T00:00:00",
                "Alarm-Endzeitpunkt": "1900-07-25T00:00:01",
                "machineid": m_rec[k],
                "Status": "No Status Data",
            }
            # append the new row to the df
            dict[k] = dict[k].append(new_row1, ignore_index=True)

            new_row2 = {
                "Alarm-ID": np.NaN,
                "Meldung": "start",
                "Quelle": "start",
                "Alarm-Startzeitpunkt": "2100-07-25T00:00:00",
                "Alarm-Endzeitpunkt": "2100-07-25T00:00:01",
                "machineid": m_rec[k],
                "Status": "No Status Data",
            }

            dict[k] = dict[k].append(new_row2, ignore_index=True)

            # sort the df, ascending: Oldest value at the top -> 1900
            dict[k] = dict[k].sort_values(by="Alarm-Startzeitpunkt", ascending=True)

            # reset the index of the df
            dict[k].reset_index(inplace=True, drop=True)

            # append the new row to the df

            s1 = []
            s2 = []
            s3 = []
            s4 = []
            s5 = []
            s6 = []
            s7 = []
            s8 = []

            for i in range(1,len(dict[k])-1):

                s1.append(dict[k]["Alarm-Startzeitpunkt"][(i)])
                s2.append(dict[k]["Status"][(i)-1])
                s3.append(dict[k]["Status"][(i) + 1])
                s4.append(dict[k]["Alarm-ID"][(i)])
                s5.append(dict[k]["Meldung"][(i)])
                s6.append(dict[k]["Quelle"][(i)])
                s7.append(dict[k]["machineid"][(i)])
                s8.append(dict[k]["Alarm-Endzeitpunkt"][(i)])

            dfnew = pd.DataFrame(
                {
                    "Alarm-Startzeitpunkt": s1,
                    "Alarm-ID": s4,
                    "Meldung": s5,
                    "Quelle": s6,
                    "machineid": s7,
                    "Alarm-Endzeitpunkt": s8,

                    "StatusDavor": s2,
                    "StatusDanach": s3,
                }
            )
            dftotal = dftotal.append(dfnew)

        dftotal = dftotal[dftotal["Alarm-ID"].notna()]
        # filter out cracy values
        dftotal = dftotal[dftotal["Alarm-Startzeitpunkt"] >= "2019-02-12T07:33:39"]
        dftotal = dftotal[dftotal["Alarm-Startzeitpunkt"] <= "2025-12-10T07:33:44"]

        # filter out statedata and new created row
        dftotal = dftotal[dftotal["Alarm-Startzeitpunkt"].notna()]

        # sort the df, ascending: Oldest value at the top
        dftotal = dftotal.sort_values(by="Alarm-Startzeitpunkt")

        # reset the index of the df
        dftotal.reset_index(inplace=True, drop=True)

        # drop duplicate rows from df
        dftotal.drop_duplicates(inplace=True)

        return dftotal

    except FileNotFoundError:

        print("No such file available in analyzestateba, Please check your Path.")

        return None





