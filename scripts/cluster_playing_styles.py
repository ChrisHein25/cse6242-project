
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import numpy as np
import os

###################### USER INPUT ########################
write_csv = True
show_plots = False
PT_drop_setpoint = 10  # drop players averaging less than X min per game
grouping_factors = ["FGA", "FG3A", "FTA", "REB", "AST", "PTS"] #['PCT_FGA_2PT', 'PCT_FGA_3PT', 'PTS_PAINT', 'PTS_2ND_CHANCE','PTS_FB', 'OREB', 'DREB', 'STL', 'BLK', 'AST', 'TOV'] #["FGA", "FG3A", "FTA", "REB", "AST", "PTS"]
##########################################################

# Step 0: Setup
os.environ["OMP_NUM_THREADS"] = '4' # set env to avoid kmeans error on Windows
grouping_factors.sort() # sort for easier reading later
print('Selected options: '+ str(grouping_factors))

# STEP 1: Import and clean full game stats data set
csv_path = "../../external/full_game_df.csv"
df = pd.read_csv(csv_path)
df = df.drop_duplicates() # drop duplicate columns
df = df.astype({"PLAYER_ID": int, "TEAM_ID": int, "GAME_ID": int, }) # recast some columns as needed

# create any pseudocolumns of interest
# df['minutes_percent'] = df['MIN']/48 # get % of game played
# df['aggressiveness'] = ((df['FGA'] - df['PTS_PAINT']) + 2*df['PTS_PAINT'] + 2*df['FTA'] + df['REB'] - df['AST'] + 3*(df['STL'] + df['BLK']))/df["MIN"]
# df = df.copy() # unfragment df

# STEP 2: Group data per player for selected stats and refilter
agg_funcs = {'PLAYER_NAME': 'first', 'PLAYER_ID': 'first', 'MIN': 'mean', 'SEASON_YEAR': pd.Series.nunique}
for col in grouping_factors:
    agg_funcs[col] = 'mean'  # add grouping factors to aggregate function for groupby
grouped_df = df.groupby(["PLAYER_ID"]).agg(agg_funcs).rename(columns={'PLAYER_ID': 'ID', 'SEASON_YEAR': 'SEASONS'}).sort_values(by=['ID'])
grouped_df = grouped_df[grouped_df['MIN'] > PT_drop_setpoint] # filter to more than 10 min playing time on average and reset index values
grouped_df = grouped_df.reset_index()
grouped_df = grouped_df.drop(columns=['PLAYER_ID'])

# STEP 3: run k-means clustering algorithm
# first normalize all player stats by playing time
grouped_df[grouping_factors] = grouped_df[grouping_factors].multiply(1 / grouped_df["MIN"], axis="index")
# rename columns to account for normalization
grouping_factors_norm = []
tag = "_PER_MIN"
for col in grouping_factors:
   grouped_df = grouped_df.rename(columns={col: col+tag})
   grouping_factors_norm.append(col+tag)

features = grouped_df[grouping_factors_norm].to_numpy()
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features) # feature scaling (must transform all parameters to the same scale)

# try multiple k-means to determine optimum number of groups
kmeans_kwargs = {"init": 'random', "n_init": 10, "max_iter": 300, "random_state": 42}

sse = []
silhouette_coeffs = []
r = range(2, 11)
for k in r:
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(scaled_features)
    sse.append(kmeans.inertia_)
    score = silhouette_score(scaled_features, kmeans.labels_)
    silhouette_coeffs.append(score)

if show_plots:
    plt.style.use("fivethirtyeight")
    plt.plot(r, sse)
    plt.xticks(r)
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.show()

    plt.style.use("fivethirtyeight")
    plt.plot(r, silhouette_coeffs)
    plt.xticks(r)
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Coefficient")
    plt.show()

# use optimum k from Elbow Method
kl = KneeLocator(r, sse, curve="convex", direction="decreasing")
k_opt = kl.elbow


kmeans = KMeans(n_clusters=k_opt, **kmeans_kwargs)
kmeans.fit(scaled_features)
# get 3 nearest neighbors to use in Graph (set as 4 bc it also finds itself first)
nbrs = NearestNeighbors(n_neighbors=4, algorithm='auto').fit(scaled_features)
distances, indices = nbrs.kneighbors(scaled_features)

print('k, sse')
print(str(k_opt), str(kmeans.inertia_))

n_indices = pd.DataFrame(data=indices, columns=["ind", "n1", "n2", "n3"])
n_distances = pd.DataFrame(data=distances, columns=["origin", "d1", "d2", "d3"])
neighbors_df = n_indices.merge(n_distances, left_index=True, right_index=True)

grouped_df['group'] = kmeans.labels_ # add grouping back into groupby table
df_final = grouped_df.merge(neighbors_df, left_index=True, right_index=True) # merge neighbor info into final df

df_final['id1'] = df_final['n1'].apply(lambda x: df_final.iloc[[x]]['ID'].values[0])
df_final['id2'] = df_final['n2'].apply(lambda x: df_final.iloc[[x]]['ID'].values[0])
df_final['id3'] = df_final['n3'].apply(lambda x: df_final.iloc[[x]]['ID'].values[0])

if write_csv:
    df_final.to_csv("output_data/player_clusters_py.csv", index=False)

print('done')



