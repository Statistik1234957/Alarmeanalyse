import numpy as np

def dtree(df):

    " This function contains the decision tree for the status computation"

    if ("mode" and "isanyaxismoving" and "isdisturbed") in df.columns:

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
        default = "No_Status_Data"

        df["Status"] = np.select(conditions, values, default)

    else:
        df["Status"] = "No_Status_Data"

    return df