import sqlalchemy as db
from sqlalchemy import exc
import database
from config_utils import ConfigUtils

cfg = ConfigUtils()
connectionstring = cfg.read_cfgvalue("DB","databank")

try:
    # establish connection to DB
    engine = db.create_engine(connectionstring)
    connection = engine.connect()

    # get the master Dataframe
    df_state = database.get_df_from_sql(database.get_state_query(), connection)

    # get the detailed df
    df_channel = database.get_df_from_sql(database.get_channel_query(), connection)

except exc.SQLAlchemyError as e:
    print(e)
