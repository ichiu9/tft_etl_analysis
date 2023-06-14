# # Transform Data


import pandas as pd


select_query_matches = '''SELECT * FROM matches LIMIT 10;'''
q_vars = ""
execute_sql(select_query_matches, q_vars, cur, conn)
matches_results = cur.fetchall()
list_matches=[]
for row in matches_results:
    current_match = [row[0], epoch_to_date(row[1]), int(row[2]/60)]
    list_matches.append(current_match)

df_matches = pd.DataFrame(list_matches, columns=['Match ID', 'Datetime', 'Length'])

#df_matches

#--------------------------------------------------------------------------------------------

select_query_players_stats = '''SELECT * FROM player_stats LIMIT 10;'''
q_vars = ""
execute_sql(select_query_players_stats, q_vars, cur, conn)
players_stats_results = cur.fetchall()

players_list=[]
for row in players_stats_results:
    current_player = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], int(row[7]/60), row[8]]
    players_list.append(current_player)
    
df_players = pd.DataFrame(players_list, columns=['m_id', 'puuid', 'gold_left', 'last_round', 'level', 'placement', 'players_eliminated', 'time_eliminated', 'total_damage_to_players'])

#df_players
#--------------------------------------------------------------------------------------------

select_query_traits = '''SELECT * FROM traits LIMIT 40;'''
q_vars = ""
execute_sql(select_query_traits, q_vars, cur, conn)
traits_results = cur.fetchall()

traits_list=[]
for row in traits_results:
    trait_color = row[4]
    if row[4] == 0:
        trait_color = "Gray"
    elif row[4] == 1:
        trait_color = "Bronze"
    elif row[4] == 2:
        trait_color = "Silver"
    elif row[4] == 3:
        trait_color = "Gold"
    elif row[4] == 4:
        trait_color = "Prismatic"

    current_trait = [row[0], row[1], row[2], row[3], trait_color, row[5], row[6], row[5]/row[6]]
    traits_list.append(current_trait)
    
df_traits = pd.DataFrame(traits_list, columns=["m_id", "puuid", "trait_name", "num_units", "style", "trait_tier_current", "trait_tier_total", "trait_ratio"])

df_traits


