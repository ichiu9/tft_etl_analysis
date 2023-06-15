#!/usr/bin/env python
# coding: utf-8

# # Pulling data from Riot APIs

#from IPython import get_ipython
from configs.pgdbconfig import *
from configs.riotconfig import *
from modules.psycop_modules.createConnection import *
from modules.psycop_modules.misc import *
from modules.sql_modules.pgCreate import *
from modules.sql_modules.pgDrop import *
from modules.sql_modules.pgInsert import *

from collections.abc import Mapping
import json
import psycopg2
import datetime
import requests


# ## Get Summoner Info

summoner = requests.get("{}/tft/summoner/v1/summoners/by-name/{}?api_key={}".format(riotpath, ign, apikey))
summonerdata = json.loads(json.dumps(summoner.json(), indent = 4))
jprint(summonerdata)

# ## Get Match Ids from Summoner
matchids = requests.get("{}/tft/match/v1/matches/by-puuid/{}/ids?count=50&api_key={}".format(americapath, summonerdata['puuid'], apikey))
matchlist = json.loads(json.dumps(matchids.json(), indent = 4))
jprint(matchlist)

# ## Get Match Data and set as 'data'
match = requests.get("{}/tft/match/v1/matches/{}?api_key={}".format(americapath, matchlist[0], apikey))
data = json.loads(json.dumps(match.json(), indent = 4))

# ## Write Match data to a file
with open('results.json', 'w') as fp:
    json.dump(data, fp)

# ### Execute SQL Queries

conn, cur = create_connection(pghost, pgdb, pguser, pgpassword)

# Drop and Create Tables
drop_tables(cur, conn)
create_tables(cur, conn)


# ### Looping through matches provided from matchlist API and pushing matchdata to Postgres

# Loop through match list
for i in range(len(matchlist)):
    match = requests.get("{}/tft/match/v1/matches/{}?api_key={}".format(americapath, matchlist[i], apikey))
    data = json.loads(json.dumps(match.json(), indent = 4))
    m_id = data["metadata"]["match_id"]
    p_list = data["info"]["participants"]
    
    # POPULATE MATCHES TABLE
    matches_vars = (m_id ,data["info"]["game_datetime"],data["info"]["game_length"])
    execute_sql(matches_sql, matches_vars, cur, conn)
        
    # Loop through list of participants
    for j in range(len(p_list)):
        
        # Set reusable variables at the participants level
        traits = p_list[j]["traits"]
        augments = p_list[j]["augments"]
        units = p_list[j]["units"]
        puuid = p_list[j]["puuid"]
        
        # POPULATE PLAYERS_IN_MATCH TABLE
        players_in_match_vars = (m_id, puuid)
        execute_sql(players_in_match_sql, players_in_match_vars, cur, conn)
        
        # POPULATE PLAYERS_STATS TABLE
        player_stats_vars = (m_id, puuid, p_list[j]["gold_left"], p_list[j]["last_round"], p_list[j]["level"], p_list[j]["placement"], p_list[j]["players_eliminated"], p_list[j]["time_eliminated"], p_list[j]["total_damage_to_players"])
        execute_sql(players_stats_sql, player_stats_vars, cur, conn)

        # Loop through augments and push to db
        for a in range(len(augments)): 
            augment_vars = (m_id, puuid, augments[a], a+1)
            execute_sql(augments_sql,augment_vars, cur, conn)
        
        # Loop through traits and push to db
        for t in range(len(traits)):
            trait_vars = (m_id, puuid, traits[t]["name"], traits[t]["num_units"], traits[t]["style"], traits[t]["tier_current"], traits[t]["tier_total"])
            execute_sql(traits_sql, trait_vars, cur, conn)
            
        # Loop through units and items and push to db
        unit_dup = []
        for u in range(len(units)):
            copy = 1
            unit_search = [m_id, puuid, units[u]["character_id"], units[u]["rarity"], units[u]["tier"]]
            if(unit_search in unit_dup):
                copy += 1
                unit_vars = (m_id, puuid, units[u]["character_id"], units[u]["rarity"], units[u]["tier"], copy)
                execute_sql(units_sql,unit_vars, cur, conn)
                for item in units[u]["itemNames"]:
                    item_vars = (m_id, puuid, units[u]["character_id"], units[u]["rarity"], units[u]["tier"], copy, item)
                    execute_sql(items_sql, item_vars, cur, conn)
            else:
                unit_vars = (m_id, puuid, units[u]["character_id"], units[u]["rarity"], units[u]["tier"], copy)
                execute_sql(units_sql,unit_vars, cur, conn)
                unit_dup.append(unit_search)
                for item in units[u]["itemNames"]:
                    item_vars = (m_id, puuid, units[u]["character_id"], units[u]["rarity"], units[u]["tier"], copy, item)
                    execute_sql(items_sql, item_vars, cur, conn)
