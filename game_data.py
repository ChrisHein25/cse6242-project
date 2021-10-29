# CSE 6242 Group 9 Project
# Python script to access nba.com stat data and pull stats on a per-game basis.
# Output is a table consisting of individual player stats for each NBA game played by each team for the past X seasons

from nba_api.stats.static import players
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import teams
from nba_api.stats.endpoints import playergamelog, playergamelogs

from datetime import datetime
import pandas as pd
from pandasql import sqldf

# setup helper functions
mysql = lambda q: sqldf(q, globals()) # setup to run sql queries on data

# enter starting and ending seasons of interest
season_start_startyear = 2003
seasons_end_startyear = 2018 # starting season year, eg 2019 would be 2019-2020 season
seasons = list(range(season_start_startyear, seasons_end_startyear+1))

# grab all NBA players
player_dict = players.get_players() # dictionary of every player who has played in the NBA

# for every season of interest, call PlayerGameLogs to get game stats from that season
frames = []
for i, season in enumerate(seasons):
    season_str = str(season)+"-"+str(season+1)[2:]
    df = playergamelogs.PlayerGameLogs(season_nullable=season_str).get_data_frames()[0]
    frames.append(df)
game_data = pd.concat(frames)
game_data = game_data.drop(columns=[
    "GP_RANK","W_RANK","L_RANK","W_PCT_RANK","MIN_RANK","FGM_RANK","FGA_RANK","FG_PCT_RANK","FG3M_RANK","FG3A_RANK",
    "FG3_PCT_RANK","FTM_RANK","FTA_RANK","FT_PCT_RANK","OREB_RANK","DREB_RANK","REB_RANK","AST_RANK","TOV_RANK",
    "STL_RANK","BLK_RANK","BLKA_RANK","PF_RANK","PFD_RANK","PTS_RANK","PLUS_MINUS_RANK","NBA_FANTASY_PTS_RANK",
    "DD2_RANK","TD3_RANK","VIDEO_AVAILABLE_FLAG"
]) # remove unneeded ranking columns
game_data = game_data.drop_duplicates() # drop any duplicate rows
game_data['GAME_DATE']= pd.to_datetime(game_data['GAME_DATE']) # clean up game date column to pd date
game_data['GAME_DATE'] = game_data['GAME_DATE'].dt.date # eliminate time part of datetime column (all 0's anyway)

# the resulting dataframe game_data contains core player stats on a per game basis for every player for every game in the season range selected
game_data.to_csv("game_data.csv", index=False) # write to CSV

# query the dataframe with SQL
res = mysql(""" select * from game_data where season_year="2015-16"; """)

# TODO - pull more unique/advanced stats next + player biometric and characteristic data for that season
# TODO - merge injury data