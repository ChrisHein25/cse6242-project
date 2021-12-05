
from nba_api.stats.static import players
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonplayerinfo, boxscoreadvancedv2, boxscoremiscv2, boxscoreplayertrackv2, boxscorescoringv2

import time
import pandas as pd
import os
from pandasql import sqldf

# grab all NBA players
player_dict = players.get_players()  # dictionary of every player who has played in the NBA

df = pd.DataFrame()

def grab_data():
    info = commonplayerinfo.CommonPlayerInfo(player_id=player['id']).get_data_frames()

print('Running...')
for ind, player in enumerate(player_dict):
    run = True
    while run:
        count = 0
        try:
            info = commonplayerinfo.CommonPlayerInfo(player_id=player['id']).get_data_frames()
            run = False
            time.sleep(0.5)
        except:
            count = count + 1
            if count > 4:
                break
            print('Try {}. Error reaching API. Trying again...'.format(count))
    if count > 4:
        break
    row = pd.DataFrame()
    for entry in info:
        if len(entry) == 1:
            row = pd.concat([row, entry], axis=1)
    if len(df) == 0:
        df = pd.concat([df, row], axis=1)
    else:
        df = pd.concat([df, row], ignore_index=True)
    print('{:.2f}% done'.format((ind + 1) * 100 / len(player_dict)))

df.to_csv('player_metadata.csv', index=False)


#player_stats = cumestatsplayer.CumeStatsPlayer(player_id='1234')

print('hi')