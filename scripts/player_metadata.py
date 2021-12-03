
from nba_api.stats.static import players
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonplayerinfo, boxscoreadvancedv2, boxscoremiscv2, boxscoreplayertrackv2, boxscorescoringv2

import pandas as pd
import os
from pandasql import sqldf

# grab all NBA players
player_dict = players.get_players()  # dictionary of every player who has played in the NBA

df = pd.DataFrame()
for ind, player in enumerate(player_dict):
    print('Evaluating player {}/{}'.format(ind+1, len(player_dict)))
    info = commonplayerinfo.CommonPlayerInfo(player_id=player['id']).get_data_frames()
    row = pd.DataFrame()
    for entry in info:
        if len(entry) == 1:
            row = pd.concat([row, entry], axis=1)
    if len(df) == 0:
        df = pd.concat([df, row], axis=1)
    else:
        df = pd.concat([df, row], ignore_index=True)


#player_stats = cumestatsplayer.CumeStatsPlayer(player_id='1234')

print('hi')