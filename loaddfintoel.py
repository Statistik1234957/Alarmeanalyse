from elasticsearch import Elasticsearch, helpers
from config_utils import ConfigUtils


def load_df_into_elasticsearch(df, indexname):

    # get path from config file
    cfg = ConfigUtils()
    elastichost = cfg.read_cfgvalue("elasticsearch", "elastichost")
    elasticport = cfg.read_cfgvalue("elasticsearch", "elasticport")

    es = Elasticsearch([{"host": elastichost, "port": elasticport}])

    #  create a unique column for your dataframe
    global a
    a = 0

    def id(x):
        global a
        a = a + 1

        return a

    cols = df.columns

    try:
        df["ID"] = df[cols[0]].apply(id)
        exceptionocurred = 0

    except IndexError:
        exceptionocurred = 1

    source = {}

    def generator(df):

        df = df.to_dict("records")

        for a, line in enumerate(df):

            for l in range(len(cols)):
                source[cols[l]] = line.get(cols[l], ["No Data"])

            yield {"_index": indexname, "_id": line.get("ID"), "_source": source}

    #  load df into elasticsearch
    helpers.bulk(es, generator(df))

    if exceptionocurred == 0:
        print("Loaded sucessfully under indexname: " + str(indexname))
    else:
        print("Your Dataframe is empty and thus can't be loaded into Elasticsearch")

    return None
