
" This file contains the decision tree for the status computation"

import numpy as np

def dtree(df):
    conditions = [
        (df["mode"] == "Automatic") & (df["isanyaxismoving"] == True),
        (df["mode"] == "Automatic")
        & (df["isanyaxismoving"] == False)
        & (df["isdisturbed"] == True),
        (df["mode"] == "Automatic")
        & (df["isanyaxismoving"] == False)
        & (df["isdisturbed"] == False),
        (df["mode"] != "Automatic") & (df["isanyaxismoving"] == True),
        (df["mode"] != "Automatic")
        & (df["isanyaxismoving"] == False)
        & (df["isdisturbed"] == True),
        (df["mode"] != "Automatic")
        & (df["isanyaxismoving"] == False)
        & (df["isdisturbed"] == False),
    ]
    values = [
        "Automatik",
        "Stoerung",
        "Ruhezustand",
        "Manuell",
        "Stoerung Manuell",
        "Ruhezustand Manuell",
    ]

    df["Status"] = np.select(conditions, values)

    return df