
import time
import pandas as pd
import os
from pandasql import sqldf

cwd = os.getcwd()
csv_path = cwd + "../pathtofile"

# setup helper functions
mysql = lambda q: sqldf(q, globals()) # setup to run sql queries on data
sort_order = ["GAME_ID", "TEAM_ID", "PLAYER_ID"] # sorting order used throughout






