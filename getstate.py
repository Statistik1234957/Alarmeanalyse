import pandas as pd
import dctreestatus
import function_collector
from config_utils import ConfigUtils

def get_status():

    # gets the paths from the Files from the config file
    cfg = ConfigUtils()
    mode_path = cfg.read_cfgvalue("Dstate", "datamode")
    disturbed_path = cfg.read_cfgvalue("Dstate", "dataisdisturbed")
    axismoving_path = cfg.read_cfgvalue("Dstate", "dataaxismoving")

    #reads in the Data
    datamode = pd.read_csv(mode_path, sep=";", header=0, low_memory=False)
    datadisturbed = pd.read_csv(disturbed_path, sep=";", header=0, low_memory=False)
    dataaxismoving = pd.read_csv(axismoving_path, sep=";", header=0, low_memory=False)

    # Format the Date column
    datamode[["timestamp", "x"]] = datamode["timestamp"].str.split(".", expand=True)
    datadisturbed[["timestamp", "x"]] = datadisturbed["timestamp"].str.split(".", expand=True)
    dataaxismoving[["timestamp", "x"]] = dataaxismoving["timestamp"].str.split(".", expand=True)

    # Format the Date column
    datamode[["timestamp", "y"]] = datamode["timestamp"].str.split("+", expand=True)
    datadisturbed[["timestamp", "y"]] = datadisturbed["timestamp"].str.split("+", expand=True)
    dataaxismoving[["timestamp", "y"]] = dataaxismoving["timestamp"].str.split("+", expand=True)

    # drop the rest
    datamode = datamode.drop(["x","y"], axis=1)
    datadisturbed = datadisturbed.drop(["x","y"], axis=1)
    dataaxismoving = dataaxismoving.drop(["x","y"], axis=1)

    # get machineidnames as list
    midmode = datamode["machineid"].unique().tolist()
    middis = datadisturbed["machineid"].unique().tolist()
    midany = dataaxismoving["machineid"].unique().tolist()
    commlist = list(set(midmode).intersection(middis))
    total = list(set(commlist).intersection(midany))

    # for each machineid and then combine the dataframe
    d = {}
    df = pd.DataFrame()

    for i in range(len(total)):
        d[i] = function_collector.datamachineid_state(datamode, datadisturbed, dataaxismoving, total[i])
        function_collector.fillup(d[i])
        dctreestatus.dtree(d[i])
        df = df.append(d[i])

    # rename the column for integration
    df = df.rename(columns={"timestamp": "Alarm-Startzeitpunkt"})

    # sort the df, ascending: Oldest value at the top -> 2001
    df = df.sort_values(by="Alarm-Startzeitpunkt")

    #drop the one atrificial created row
    p = df[df['Alarm-Startzeitpunkt'] == '2001-07-25T00:00:00'].index
    df = df.drop(p)

    #convert to iso format
    function_collector.fromat_timestamp_toiso(df)

    # slect only the relevant Data
    df = df[["Alarm-Startzeitpunkt","machineid", "Status"]]

    #reset the index of the df
    df.reset_index(inplace=True,drop=True)

    #drop duplicate rows from df
    df.drop_duplicates(inplace= True)

    return df
