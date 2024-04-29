
"""
This will post trip data every second to public.trips table in postgres as well as post messages to the kafka server.

"""

#%%
import logging
import os
import json
import traceback
import pandas as pd
import time
from db_handler import DatabaseHandler
# from kafka import KafkaProducer
from rp_handler import KafkaProducer
#%%
#Update the redpanda server when running in docker
bootstrap_servers=[os.environ.get('BOOTSTRAP_SERVERS', "localhost:19092")]

data_refresh_interval = 1

#%%
#Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s :: %(levelname)s :: %(filename)s :: %(funcName)s :: %(message)s",
)

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

#%%
#Set up database handler
db = DatabaseHandler()

#create a kafka producer instance . update localhost to server name in docker
# producer = KafkaProducer(bootstrap_servers=['localhost:19092'], value_serializer=lambda m: json.dumps(m).encode('ascii'), retries=3)
producer = KafkaProducer(topic_name='latest_locations', client_id='redpanda')

#%%
#load the data source
df_trip = pd.read_csv('fake_data_generator/trips.csv').sort_values('measurement_sequence')
df_trip.head()

#test the connection
trip_data = json.loads(df_trip.iloc[0].to_json())
db.add_trip(trip_data)

#create a view foror the realtime location application
db.create_view_trip()


#%%
#Post data every data_refresh_interval second
try: 

    for i in range(len(df_trip)):

        #create the trip row data
        trip_data = json.loads(df_trip.iloc[i].to_json())

        #podt data to postgres
        db.add_trip(trip_data)

        #alternatively we can post data to redpanda / kafka
        producer.send_messages({ str(trip_data)})

        time.sleep(data_refresh_interval)

except Exception as e:
        logger.error(f"Error: {str(e)}.")
        logger.error(traceback.format_exc())

#%%