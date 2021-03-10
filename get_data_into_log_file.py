import getrecstatus
from datetime import datetime

"""
This file executes the entire Code.
Enter the Machines you want to anaylze in the machinelist.
"""

# Machineslist
machinelist = ["G352-2114", "G352-2188"]

# Data_Rec with state
print("Starting Loading Data:")
datarecws = getrecstatus.get_recws(machinelist)
print("Finished Loading Data:")

#write your Data into a log file with name: filename:
with open("filename.log", "a") as logfile:

    for index,value in datarecws.iterrows():

        alarm_startzeitpunkt = value["Alarm-Startzeitpunkt"]
        alarm_startzeitpunkt = datetime.strptime(alarm_startzeitpunkt, '%Y-%m-%dT%H:%M:%S')
        alarm_startzeitpunkt = alarm_startzeitpunkt.strftime('%b %d %H:%M:%S')
        logfile.write(f"{alarm_startzeitpunkt} CEST | [de-elk-stack-advanced] | grobbeat | Response from sensor (openfiles-total): {value.to_json()} \n")


print("Finished appending to the file")