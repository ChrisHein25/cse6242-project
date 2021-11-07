# CSE 6242 Group 9 Project
# Python script to access injury timeseries data in text format build a db where every unique injury occurance is an individual row

import pandas as pd
import os

cwd = os.getcwd()
csv_path = cwd + "/output_data"

# 0. Import data, do basic cleaning, and cast columns
df = pd.read_csv("input_data/injuries_2010-2020.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.drop_duplicates()
print('Original rows: '+str(len(df)))


# 1. Drop where Acquired not NAN
df = df[~df['Acquired'].notna()]
print('Rows after 1: '+str(len(df)))

# 2. Drop Acquired column, rename Relinquished to Player, then drop any row with mention of 'activat'
df = df.drop(columns=['Acquired'])
df = df.rename(columns={"Relinquished": "Player"})
df = df[~df['Notes'].str.contains("activat")]
print('Rows after 2: '+str(len(df)))

# 3. Order by player, then date to see each player's timeline
df = df.sort_values(by=['Player', 'Date'])
#df.to_csv(csv_path+"/testfile.csv", index=False)# 4. Apply Maggie's OpenRefine logic to categorize into Injury and Non-injury (sickness, etc)

# 5. Apply algorithm to check for repeat or near entries

print('hi')