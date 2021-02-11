import loaddfintoel
import analyzestateba
import getrecstatus
import logfiles
import createindexpattern

"1. get all Data_Frames and load them into Elasticsearch"

# Machineslist
machinelist = ["\G352-2114", "\G352-2188"]

# Data_Rec with state
print("Starting Loading Rec-Data")
#datarecws = getrecstatus.get_recws(machinelist)
#datarecws.to_csv("Data_Rec_Status",index= False)

#Stoplogdata
print("Starting Loading Stoplog-Data")
#datastoplog = logfiles.getstoplog_total()
#datastoplog.to_csv("Data_Stoplog",index= False)

#Data Status before and after "Störung"
print("Starting Loading Rec-Data with State before and after")
datastatebeaf = analyzestateba.getstatebeaf(machinelist)
#datastatebeaf.to_csv("Data_Status_BE_AF",index= False)


# Load df's into elasticsearch

"Be careful, the indexname must be in full lower case"
print("Starting Loading Data into Elasticsearch")
#loaddfintoel.load_df_into_elasticsearch(datarecws, indexname="recdata")
loaddfintoel.load_df_into_elasticsearch(datastatebeaf, indexname="state_be_af")
#loaddfintoel.load_df_into_elasticsearch(datastoplog, indexname="stoplogdata")


# create index pattern in Kibana
print("Starting creating Index Pattern in Kibana")

#createindexpattern.create_index_pattern("recdata")
createindexpattern.create_index_pattern("state_be_af")
#createindexpattern.create_index_pattern("stoplogdata")

