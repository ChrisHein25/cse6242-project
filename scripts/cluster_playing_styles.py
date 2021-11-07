
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import numpy as np

# STEP 1: Import and clean full game stats data set
csv_path = "../../external/full_game_df.csv"
df = pd.read_csv(csv_path)
df = df.drop_duplicates() # drop duplicate columns
df = df.astype({"PLAYER_ID": int, "TEAM_ID": int, "GAME_ID": int, }) # recast some columns as needed

# create pseudocolumns on interest
df['minutes_percent'] = df['MIN']/48 # get % of game played
df['aggressiveness'] = ((df['FGA'] - df['PTS_PAINT']) + 2*df['PTS_PAINT'] + 2*df['FTA'] + df['REB'] - df['AST'] + 3*(df['STL'] + df['BLK']))/df["MIN"]

# STEP 2: Group data per player for selected stats and refilter
agg_funcs = {'PLAYER_NAME': 'first', 'PLAYER_ID': 'first', 'MIN': 'mean', 'SEASON_YEAR': pd.Series.nunique,'FGA': 'mean', 'FG3A': 'mean', 'FTA': 'mean', 'REB': 'mean', 'AST': 'mean', 'PTS': 'mean'}
grouped_df = df.groupby(["PLAYER_ID"]).agg(agg_funcs).rename(columns={'PLAYER_ID': 'ID', 'SEASON_YEAR': 'SEASONS'}).sort_values(by=['ID'])
grouped_df = grouped_df[grouped_df['MIN'] > 10] # filter to more than 10 min playing time on average and reset index values
grouped_df = grouped_df.reset_index()
grouped_df = grouped_df.drop(columns=['PLAYER_ID'])

# STEP 3: run k-means clustering algorithm
features = grouped_df[["FGA", "FG3A", "FTA", "REB", "AST", "PTS"]].to_numpy()
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features) # feature scaling (must transform all parameters to the same scale)

k = 4  # hyperparameter
kmeans = KMeans(init='random', n_clusters=k, n_init=10, max_iter=300, random_state=42, verbose=1)
kmeans.fit(scaled_features)
nbrs = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(scaled_features)
distances, indices = nbrs.kneighbors(scaled_features)

n_indices = pd.DataFrame(data=indices, columns=["ind", "n1", "n2", "n3"])
n_distances = pd.DataFrame(data=distances, columns=["origin", "d1", "d2", "d3"])
neighbors_df = n_indices.merge(n_distances, left_index=True, right_index=True)

grouped_df['group'] = kmeans.labels_ # add grouping back into groupby table
df_final = grouped_df.merge(neighbors_df, left_index=True, right_index=True) # merge neighbor info into final df

df_final['id1'] = df_final['n1'].apply(lambda x: df_final.iloc[[x]]['ID'].values[0])
df_final['id2'] = df_final['n2'].apply(lambda x: df_final.iloc[[x]]['ID'].values[0])
df_final['id3'] = df_final['n3'].apply(lambda x: df_final.iloc[[x]]['ID'].values[0])

df_final.to_csv("output_data/player_clusters_py.csv")

print('done')



