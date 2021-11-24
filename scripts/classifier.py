import pandas as pd
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import numpy as np
import os


class Classifier:
    def __init__(self, csv_path=None, grouping_factors=None, norm_knn_by_min=True, min_games_played=10, pt_drop_setpoint=10, n_neighbors=3, write_csv=True, show_plots=False, prints=False):
        if isinstance(csv_path, type(None)) or isinstance(csv_path, type(None)):
            raise Exception('Please make sure csv_path and grouping_factors are specified.')

        # required
        self.csv_path = csv_path
        self.grouping_factors = grouping_factors  # list of form ["FGA", "FG3A", "FTA", "REB", "AST", "PTS"]

        # optional
        self.PT_drop_setpoint = pt_drop_setpoint  # default to dropping players with less than 10 min avg playing time
        self.min_games_played = min_games_played  # default to a minimum of X games played
        self.n_neighbors = n_neighbors  # number of neighbors for knn
        self.norm_knn_by_min = norm_knn_by_min
        self.write_csv = write_csv
        self.show_plots = show_plots
        self.prints = prints

    def cluster(self, no_df=False):

        # Step 0: Setup
        os.environ["OMP_NUM_THREADS"] = '4'  # set env to avoid kmeans error on Windows machine
        grouping_factors = self.grouping_factors
        grouping_factors.sort()  # sort for easier reading later
        if self.prints:
            print('Selected options: ' + str(grouping_factors))

        # STEP 1: Import and clean full game stats data set
        csv_path = self.csv_path
        df = pd.read_csv(csv_path)
        df = df.drop_duplicates()  # drop duplicate columns
        df = df.astype({"PLAYER_ID": int, "TEAM_ID": int, "GAME_ID": int, })  # recast some columns as needed

        # create any pseudocolumns of interest
        # df['minutes_percent'] = df['MIN']/48 # get % of game played
        # df['aggressiveness'] = ((df['FGA'] - df['PTS_PAINT']) + 2*df['PTS_PAINT'] + 2*df['FTA'] + df['REB'] - df['AST'] + 3*(df['STL'] + df['BLK']))/df["MIN"]
        # df = df.copy() # unfragment df

        # STEP 2: Group data per player for selected stats and refilter
        agg_funcs = {'PLAYER_NAME': 'first', 'PLAYER_ID': 'first', 'MIN': 'mean', 'GAME_ID': pd.Series.nunique, 'SEASON_YEAR': pd.Series.nunique}
        for col in grouping_factors:
            agg_funcs[col] = 'mean'  # add grouping factors to aggregate function for groupby
        grouped_df = df.groupby(["PLAYER_ID"]).agg(agg_funcs).rename(columns={'PLAYER_ID': 'ID', 'GAME_ID': 'GAMES', 'SEASON_YEAR': 'SEASONS'}).sort_values(by=['ID'])
        grouped_df = grouped_df[grouped_df['MIN'] >= self.PT_drop_setpoint] # filter to more than 10 min playing time on average and reset index values
        grouped_df = grouped_df[grouped_df['GAMES'] >= self.min_games_played]  # filter for games played
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
        scaler.fit(features)
        scaled_features = scaler.transform(features)
        #scaled_features = scaler.fit_transform(features_scaled) # feature scaling (must transform all parameters to the same scale)

        # try multiple k-means to determine optimum number of groups
        kmeans_kwargs = {"init": 'random', "n_init": 10, "max_iter": 300, "random_state": 42}

        sse = []
        silhouette_coeffs = []
        r = range(4, 12)  # evaluate between 4 to 12 playing style groups
        for k in r:
            kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
            kmeans.fit(scaled_features)
            sse.append(kmeans.inertia_)
            score = silhouette_score(scaled_features, kmeans.labels_)
            silhouette_coeffs.append(score)

        if self.show_plots:
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
        detectedKnee = True
        try:
            kl = KneeLocator(r, sse, curve="convex", direction="decreasing")
            k_opt = kl.elbow

            kmeans = KMeans(n_clusters=k_opt, **kmeans_kwargs)
            kmeans.fit(scaled_features)

        except Exception as e:
            print(e.args[0])
            print('Error in kmeans fitting. Possibly did not converge. Returning 1 for grouping.')
            k_opt = 1
            sse = 9999999999
            df = pd.DataFrame()  #empty df
            if no_df:
                return k_opt, sse
            else:
                return df, k_opt, sse

        # TODO: build out the option to NOT normalize by minutes
        # if self.norm_knn_by_min: do some stuff
        # get nearest neighbors to use in Graph (+1 because it'll also match itself too)
        nbrs = NearestNeighbors(n_neighbors=self.n_neighbors+1, algorithm='auto').fit(scaled_features)
        distances, indices = nbrs.kneighbors(scaled_features)

        if self.prints:
            print('k, sse')
            print(str(k_opt), str(kmeans.inertia_))

        n_indices = pd.DataFrame(data=indices, columns=["ind", "n1", "n2", "n3"])
        n_distances = pd.DataFrame(data=distances, columns=["origin", "d1", "d2", "d3"])
        neighbors_df = n_indices.merge(n_distances, left_index=True, right_index=True)

        grouped_df['group'] = kmeans.labels_ # add grouping back into groupby table
        df_final = grouped_df.merge(neighbors_df, left_index=True, right_index=True) # merge neighbor info into final df

        # TODO: make a flexible amount of neighbors
        df_final['id1'] = df_final['n1'].apply(lambda x: df_final.iloc[[x]]['ID'].values[0])
        df_final['id2'] = df_final['n2'].apply(lambda x: df_final.iloc[[x]]['ID'].values[0])
        df_final['id3'] = df_final['n3'].apply(lambda x: df_final.iloc[[x]]['ID'].values[0])

        # final cleanup
        df_final = df_final.drop(columns=['ind', 'n1', 'n2', 'n3', 'origin'])

        if self.write_csv:
            # Todo: update this path
            df_final.to_csv("output_data/player_clusters_py.csv", index=False)

        if no_df:
            return k_opt, kmeans.inertia_
        else:
            return df_final, k_opt, kmeans.inertia_

