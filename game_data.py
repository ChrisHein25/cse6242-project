# CSE 6242 Group 9 Project
# Python script to access nba.com stat data and pull stats on a per-game basis.
# Output is a table consisting of individual player stats for each NBA game played by each team for the past X seasons

from nba_api.stats.static import players
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import teams
from nba_api.stats.endpoints import playergamelogs, boxscoreadvancedv2, boxscoremiscv2, boxscoreplayertrackv2, boxscorescoringv2

import time
import pandas as pd
from pandasql import sqldf

start_time = time.time()

# setup helper functions
mysql = lambda q: sqldf(q, globals()) # setup to run sql queries on data
sort_order = ["GAME_ID", "TEAM_ID", "PLAYER_ID"] # sorting order used throughout

# enter starting and ending seasons of interest
season_start_startyear = 2015
seasons_end_startyear = 2015 # starting season year, eg 2019 would be 2019-2020 season
seasons = list(range(season_start_startyear, seasons_end_startyear+1))

# grab all NBA players
player_dict = players.get_players() # dictionary of every player who has played in the NBA

# for every season of interest, call PlayerGameLogs to get game stats from that season
frames = []
for i, season in enumerate(seasons):
    season_str = str(season)+"-"+str(season+1)[2:]
    df = playergamelogs.PlayerGameLogs(season_nullable=season_str).get_data_frames()[0]
    frames.append(df)
game_df = pd.concat(frames)
game_df = game_df.drop(columns=[
    "GP_RANK","W_RANK","L_RANK","W_PCT_RANK","MIN_RANK","FGM_RANK","FGA_RANK","FG_PCT_RANK","FG3M_RANK","FG3A_RANK",
    "FG3_PCT_RANK","FTM_RANK","FTA_RANK","FT_PCT_RANK","OREB_RANK","DREB_RANK","REB_RANK","AST_RANK","TOV_RANK",
    "STL_RANK","BLK_RANK","BLKA_RANK","PF_RANK","PFD_RANK","PTS_RANK","PLUS_MINUS_RANK","NBA_FANTASY_PTS_RANK",
    "DD2_RANK","TD3_RANK","VIDEO_AVAILABLE_FLAG"
]) # remove unneeded ranking columns
game_df = game_df.drop_duplicates() # drop any duplicate rows
game_df['GAME_DATE']= pd.to_datetime(game_df['GAME_DATE']) # clean up game date column to pd date
game_df['GAME_DATE'] = game_df['GAME_DATE'].dt.date # eliminate time part of datetime column (all 0's anyway)
game_df = game_df.sort_values(by=sort_order)
# the resulting dataframe game_df contains core player stats on a per game basis for every player for every game in the season range selected
game_df.to_csv("game_df.csv", index=False) # write to CSV

# query the dataframe with SQL
#res = mysql(""" select * from game_df where season_year="2015-16"; """)


# for every game_id in the dataset, build database iteratively (takes a very long time)
game_ids = game_df["GAME_ID"].unique().tolist()
game_ids.sort()
total_games = len(game_ids)
frames = []

def merge_nba_frames(df1, df2, on_col='PLAYER_ID'):
    df = pd.merge(df1, df2, on=on_col, how='inner')
    df = df[df.columns.drop(list(df.filter(regex='_y')))]
    df.columns = df.columns.str.rstrip('_x')
    return df

for i, id in enumerate(game_ids):
    print(str(i)+"/"+str(total_games))
    df_adv = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=id).get_data_frames()[0] # want first item which is player-based (2nd is team-based)
    df_misc = boxscoremiscv2.BoxScoreMiscV2(game_id=id).get_data_frames()[0]
    df_track = boxscoreplayertrackv2.BoxScorePlayerTrackV2(game_id=id).get_data_frames()[0]
    df_scoring = boxscorescoringv2.BoxScoreScoringV2(game_id=id).get_data_frames()[0]
    # df_hustle = hustlestatsboxscore.HustleStatsBoxScore(game_id=id).get_data_frames()  # hit or miss with if each game has data
    #df_playbyplay = playbyplayv2.PlayByPlayV2(game_id=id).get_data_frames() # playbyplay data if need be
    # merge all dataframes
    df_temp = merge_nba_frames(df_adv, df_misc)
    df_temp2 = merge_nba_frames(df_temp, df_track)
    df = merge_nba_frames(df_temp2, df_scoring)
    frames.append(df)
advanced_game_df = pd.concat(frames)
advanced_game_df.to_csv("advanced_game_df.csv", index=False) # write to CSV

# join with larger game dataset (just fyi you lose some possible injury data (look at df value))
full_game_df = pd.merge(game_df, advanced_game_df, on=['GAME_ID', 'TEAM_ID', 'PLAYER_ID'], how='inner').sort_values(by=['GAME_ID']).sort_values(by=sort_order)
# remove repeat columns
full_game_df = full_game_df[full_game_df.columns.drop(list(full_game_df.filter(regex='_y')))]
# restore original column names before merge
full_game_df.columns = full_game_df.columns.str.rstrip('_x')
full_game_df.to_csv("full_game_df.csv", index=False) # write to CSV

print("--- %s seconds ---" % (time.time() - start_time))
