import json
import pandas as pd
from tqdm import tqdm

# big query
with open('./yelp_dataset/yelp_academic_dataset_business.json') as file:
    data = []

    for line in file:
        json_data = json.loads(line)
        data.append(json_data)

# set up the master and instantiate the form that will take place in the loop
master = pd.DataFrame.from_dict(data[1], orient='index').transpose()

# loop though json elements inside the data list and build the df
for i in tqdm(range(1, len(data))):
    biz = pd.DataFrame.from_dict(data[i], orient='index').transpose()
    master = pd.concat([master, biz])

master.to_csv('./businesses.csv')
