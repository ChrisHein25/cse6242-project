from classifier import Classifier
from build_player_graph import Graph
from itertools import combinations
import pandas as pd
import time


if __name__=="__main__":

    start_time = time.time()

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

    # exclusion rules are reciprocal (if PTS in combo and FGM in combo do not consider that combo)
    exclusion_rules = {
        "PFD": "PF",
        "FGM": "PTS",
        "FG3M": "PTS",
        "OREB": "REB",
        "DREB": "REB",
        "PTS": ["PTS_2ND_CHANCE", "PTS_FB", "PTS_PAINT"]  # if pts is present, then pts_2nd_chance, etc cannot be and visa versa
    }

    # inclusion rules are not reciprocal (if FGM and FG3M in combo but not PTS_2ND_CHANCE that is okay)
    inclusion_rules = {
        "PTS_2ND_CHANCE": ["FGM", "FG3M"],  # both FGM and FG3M must be present to include pts_2nd_chance
        "PTS_FB": ["FGM", "FG3M"],
        "PTS_PAINT": ["PTS_2ND_CHANCE", "FGM", "FG3M"]
    }

    base_list = ["AST", "STL", "BLK", "PFD"]  # base list of stats that will always be included

    min_num_stats_considered = 10  # important note: we don't think any combo less than 10 could accurate summarize a basketball player
    combos_to_check = []

    def check_exclusion_rules(combo, exclusion_rules):
        for key, value in exclusion_rules.items():
            if key in combo:
                if isinstance(value, list):
                    for item in value:
                        if item in combo:
                            return False
                else:
                    if value in combo:
                        return False
            if isinstance(value, list):
                for item in value:
                    if item in combo:
                        if key in combo:
                            return False
            else:
                if value in combo:
                    if key in combo:
                        return False
        return True

    def check_inclusion_rules(combo, inclusion_rules):
        # only checking for keys in inclusion rules, could have any combo of values and be okay even if key is not there
        for key, value in inclusion_rules.items():
            if key in combo:
                if isinstance(value, list):
                    for item in value:
                        if item not in combo:
                            return False
                else:
                    if value not in combo:
                        return False
            # if isinstance(value, list):
            #     for item in value:
            #         if item in combo:
            #             if key not in combo:
            #                 return False
            # elif value in combo:
            #     if key not in combo:
            #         return False
        return True

    def check_base_list(combo, base_list):
        for item in base_list:
            if item not in combo:
                return False
        return True

    for i in range(min_num_stats_considered, len(possible_stats)):
        for combo in combinations(possible_stats, i):  # 2 for pairs, 3 for triplets, etc
            if check_exclusion_rules(combo, exclusion_rules) and check_inclusion_rules(combo, inclusion_rules) and check_base_list(combo, base_list):
                combos_to_check.append(combo)

    # run the DOE for all combinations deemed okay to check by the rules
    csv_path = "../../full_game_df.csv"

    players = [
        'Kyle Korver',
        'Ray Allen',
        'JJ Redick',
        'Danny Green',

        'Chris Paul',
        'Steve Nash',
        'Rajon Rondo',
        'Deron Williams',
        'Tony Parker',
        'Ricky Rubio',
        'Jason Kidd',

        'Dwight Howard',
        "Shaquille O'Neal",
        'Tyson Chandler',
        'DeAndre Jordan',
        'Blake Griffin',
        'Serge Ibaka',
        'JaVale McGee',

        'LeBron James',
        'James Harden',
        'Russell Westbrook',
        'Luka Doncic',
        'Dwyane Wade',
        'Anthony Davis',
        'Kobe Bryant',
        'Kevin Durant',
        'Damian Lillard',
        'Kyrie Irving',
        'Kawhi Leonard',
        'Giannis Antetokounmpo',

        'Dirk Nowitzki',
        'Tim Duncan',
        'Nikola Vucevic',
        'Nikola Jokic']

    cols = ['combo', 'k', 'inertia']
    [cols.append(player) for player in players]
    res_df = pd.DataFrame(columns=cols)
    for i, combo in enumerate(combos_to_check):
        print('Checking {}/{} combinations'.format(str(i+1), str(len(combos_to_check))))
        grouping_factors = list(combo)  # convert to list for function
        cl = Classifier(csv_path, grouping_factors, write_csv=False, prints=False)
        df, k_opt, inertia = cl.cluster()
        row = {'combo': grouping_factors, 'k': k_opt, 'inertia': inertia}
        for player in players:
            try:
                row[player] = df[df['PLAYER_NAME'] == player]['group'].tolist()[0]
            except:
                print(player)
        res_df = res_df.append(row, ignore_index=True)

    end_time = time.time()
    print('Finished. Code took {} seconds.'.format(str(end_time-start_time)))

    res_df.to_csv('doe_results.csv', index_label='index')
    print('Saved csv')

    # TODO: manually down-select

    #
    #
    # # example usage and building of Graph
    # csv_path = "C:/Users/212761772/Box/MyBox/Georgia Tech/Fall 2021/CSE6242/Project/external/full_game_df.csv"
    # grouping_factors = ["FGA", "FG3A", "FTA", "REB", "AST", "PTS"]  # ['PCT_FGA_2PT', 'PCT_FGA_3PT', 'PTS_PAINT', 'PTS_2ND_CHANCE','PTS_FB', 'OREB', 'DREB', 'STL', 'BLK', 'AST', 'TOV'] #["FGA", "FG3A", "FTA", "REB", "AST", "PTS"]
    #
    # cl = Classifier(csv_path, grouping_factors, write_csv=False, prints=True)
    # clustered_df = cl.cluster()
    #
    # # initialize Graph object
    # graph = Graph()
    #
    # df = clustered_df
    #
    # # iterate through all players, adding each's 3 nodes and edges
    # for index, row in df.iterrows():
    #     player = row['PLAYER_NAME']
    #     name_1 = df[df['ID'] == row['id1']]['PLAYER_NAME'].values[0]
    #     group_1 = df[df['ID'] == row['id1']]['group'].values[0]
    #     min_1 = df[df['ID'] == row['id1']]['MIN'].values[0]
    #     name_2 = df[df['ID'] == row['id2']]['PLAYER_NAME'].values[0]
    #     group_2 = df[df['ID'] == row['id3']]['group'].values[0]
    #     min_2 = df[df['ID'] == row['id2']]['MIN'].values[0]
    #     name_3 = df[df['ID'] == row['id3']]['PLAYER_NAME'].values[0]
    #     group_3 = df[df['ID'] == row['id3']]['group'].values[0]
    #     min_3 = df[df['ID'] == row['id3']]['MIN'].values[0]
    #
    #     # add nodes
    #     graph.add_node(row['ID'], row['PLAYER_NAME'], row['group'], row['MIN'])  # add player himself
    #     graph.add_node(row['id1'], name_1, group_1, min_1)  # add player neighbor 1
    #     graph.add_node(row['id2'], name_2, group_2, min_2)  # add player neighbor 2
    #     graph.add_node(row['id3'], name_3, group_3, min_3)  # add player neighbor 3
    #
    #     # add edges
    #     graph.add_edge(row['ID'], row['id1'])
    #     graph.add_edge(row['ID'], row['id2'])
    #     graph.add_edge(row['ID'], row['id3'])
    #
    # #graph.write_nodes_file("output_data/nodes.csv")
    # #graph.write_edges_file("output_data/edges.csv")
    #
    # print('done')

