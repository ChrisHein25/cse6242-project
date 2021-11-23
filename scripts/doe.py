from classifier import Classifier
from build_player_graph import Graph

if __name__=="__main__":
    possible_stats = [
        "FGM",
        "FGA",  # field goal attempts
        "FG3M",
        "FG3A",  # 3 point attempts
        "OREB",
        "DREB",
        "REB",
        "AST",
        "STL",
        "BLK",
        #"PF",  # fouls given
        "PFD",  # personal fouls drawn
        "PTS",
        "PTS_2ND_CHANCE",
        "PTS_FB",  # fast-break points
        "PTS_PAINT"]  # points in the paint

    exclusion_rules = {
        "FGM": "PTS",
        "FG3M": "PTS",
        "OREB": "REB",
        "DREB": "REB",
        "PTS": ["PTS_2ND_CHANCE", "PTS_FB", "PTS_PAINT"]
    }

    inclusion_rules = {
        "PTS_2ND_CHANCE": ["FGM", "FG3M"],  # both FGM and FG3M must be present to include pts_2nd_chance
        "PTS_FB": ["FGM", "FG3M"],
        "PTS_PAINT": ["FGM", "FG3M"]
    }

    # TODO: build out all the combinations making sure each combo adheres to rules

    # TODO: run all the clustering combos

    # TODO: manually down-select



    # example usage
    csv_path = "C:/Users/212761772/Box/MyBox/Georgia Tech/Fall 2021/CSE6242/Project/external/full_game_df.csv"
    grouping_factors = ["FGA", "FG3A", "FTA", "REB", "AST", "PTS"]  # ['PCT_FGA_2PT', 'PCT_FGA_3PT', 'PTS_PAINT', 'PTS_2ND_CHANCE','PTS_FB', 'OREB', 'DREB', 'STL', 'BLK', 'AST', 'TOV'] #["FGA", "FG3A", "FTA", "REB", "AST", "PTS"]

    cl = Classifier(csv_path, grouping_factors, write_csv=False, prints=True)
    clustered_df = cl.cluster()

    # initialize Graph object
    graph = Graph()

    df = clustered_df

    # iterate through all players, adding each's 3 nodes and edges
    for index, row in df.iterrows():
        player = row['PLAYER_NAME']
        name_1 = df[df['ID'] == row['id1']]['PLAYER_NAME'].values[0]
        group_1 = df[df['ID'] == row['id1']]['group'].values[0]
        min_1 = df[df['ID'] == row['id1']]['MIN'].values[0]
        name_2 = df[df['ID'] == row['id2']]['PLAYER_NAME'].values[0]
        group_2 = df[df['ID'] == row['id3']]['group'].values[0]
        min_2 = df[df['ID'] == row['id2']]['MIN'].values[0]
        name_3 = df[df['ID'] == row['id3']]['PLAYER_NAME'].values[0]
        group_3 = df[df['ID'] == row['id3']]['group'].values[0]
        min_3 = df[df['ID'] == row['id3']]['MIN'].values[0]

        # add nodes
        graph.add_node(row['ID'], row['PLAYER_NAME'], row['group'], row['MIN'])  # add player himself
        graph.add_node(row['id1'], name_1, group_1, min_1)  # add player neighbor 1
        graph.add_node(row['id2'], name_2, group_2, min_2)  # add player neighbor 2
        graph.add_node(row['id3'], name_3, group_3, min_3)  # add player neighbor 3

        # add edges
        graph.add_edge(row['ID'], row['id1'])
        graph.add_edge(row['ID'], row['id2'])
        graph.add_edge(row['ID'], row['id3'])

    #graph.write_nodes_file("output_data/nodes.csv")
    #graph.write_edges_file("output_data/edges.csv")

    print('done')

