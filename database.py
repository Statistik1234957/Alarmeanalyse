import pandas as pd


def get_df_from_sql(query, connection):

    "This function gets the data from the DB and returns a DF"

    result_set = connection.execute(query).fetchall()

    if len(result_set) == 0:
        return pd.DataFrame()

    df = pd.DataFrame(result_set)
    df.columns = result_set[0].keys()
    df = df.fillna(0)
    return df


def get_state_query():
    query = f"""
            select 
            machineid
            from public.machinealarm 
            where machineid not like 'G999%%'
            and machineid not like 'Cucumber%%'
            and machineid not like 'MOCK%%'
            group by machineid
            order by counted desc
    """

    return query

def get_channel_query():
    query = f"""
            select sequenceid, machineid, starttime                 
            from  machinealarm                        
            order by sequenceid asc           
        """
    return query


