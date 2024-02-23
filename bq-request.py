import os
from google.cloud import bigquery
import pandas as pd

# set credentials (json key file that gives access to BigQuery)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'bq-key.json'
client = bigquery.Client()

# query tabularized data
request = client.query(
    """
    SELECT * 
    FROM `ba820-proj.yelp_academic_dataset.tabularized`
    TABLESAMPLE SYSTEM (20 PERCENT)
    """
)

print('starting query')
# ensures query is completed
results = request.result()

# query results to pandas df
df = results.to_dataframe()

# send off to folder
df.to_csv('./sampled.csv')
print('done')