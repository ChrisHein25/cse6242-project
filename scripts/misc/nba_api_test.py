from nba_api.stats.static import players
import pandas as pd
player_dict = players.get_players()

player_df = pd.DataFrame(player_dict).sort_values(by=['id'])



# Use ternary operator or write function
# Names are case sensitive
bron = [player for player in player_dict if player['full_name'] == 'LeBron James'][0]
bron_id = bron['id']

# find team Ids
from nba_api.stats.static import teams
teams = teams.get_teams()
GSW = [x for x in teams if x['full_name'] == 'Golden State Warriors'][0]
GSW_id = GSW['id']

print(bron_id)










#
#
#
# # for each NBA player, grab season data for seasons of interest
# for cnt, player in enumerate(player_dict):
#     print(cnt)
#     if cnt == 0:
#         player_gamelog = playergamelog.PlayerGameLog(player_id=player['id'], season=SeasonAll.all).get_data_frames()[0]
#     else:
#         player_gamelog_to_add = playergamelog.PlayerGameLog(player_id=player['id'], season=SeasonAll.all).get_data_frames()[0]
#         frames = [player_gamelog, player_gamelog_to_add]
#         player_gamelog = pd.concat(frames)
#
# print(cnt)
# #
# playergamelog.PlayerGameLog(player_id='2544', season = SeasonAll.all)
#
# test = playergamelog.PlayerGameLog(player_id='2544', season='all')
#
# #Converts gamelog object into a pandas dataframe
# #can also convert to JSON or dictionary
# df_bron_games_all = gamelog_bron.get_data_frames()
#
# # If you want all seasons, you must import the SeasonAll parameter
# from nba_api.stats.library.parameters import SeasonAll
#
# gamelog_bron_all = playergamelog.PlayerGameLog(player_id='2544', season = SeasonAll.all)
#
# df_bron_games_all = gamelog_bron_all.get_data_frames()
#
