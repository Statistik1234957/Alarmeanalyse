import getrecstatus

# Machineslist
machinelist = ["\G352-2114", "\G352-2188"]


# Data_Rec with state
print("Starting Loading Rec-Data")
datarecws = getrecstatus.get_recws(machinelist)


with open("data_rec_ws_txt.txt", "a") as logfile:

    for index, value in datarecws.iterrows():
        logfile.write(f"Oct {index} 08:03:22 CEST | [de-elk-stack-advanced] | grobbeat | Response from sensor (openfiles-total): {value.to_json()} \n")


print("Finished appending the Rec-Data")