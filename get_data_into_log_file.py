import getrecstatus
from datetime import datetime

# Machineslist
machinelist = ["G352-2114", "G352-2188"]

# Data_Rec with state
print("Starting Loading Rec-Data:")
datarecws = getrecstatus.get_recws(machinelist)

with open("filename.log", "a") as logfile:

    for index,value in datarecws.iterrows():

        alarm_startzeitpunkt = value["Alarm-Startzeitpunkt"]
        alarm_startzeitpunkt = datetime.strptime(alarm_startzeitpunkt, '%Y-%m-%dT%H:%M:%S')
        alarm_startzeitpunkt = alarm_startzeitpunkt.strftime('%b %d %H:%M:%S')
        logfile.write(f"{alarm_startzeitpunkt} CEST | [de-elk-stack-advanced] | grobbeat | Response from sensor (openfiles-total): {value.to_json()} \n")


print("Finished appending the Rec-Data")