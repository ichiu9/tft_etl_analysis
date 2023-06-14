
matches_sql = '''
        INSERT INTO matches ("m_id", "m_datetime", "m_length") 
        VALUES (%s,%s,%s);'''
players_in_match_sql = '''
        INSERT INTO players_in_match ("m_id", "puuid") 
        VALUES (%s,%s);'''
players_stats_sql = '''
        INSERT INTO player_stats ("m_id", "puuid", "gold_left", "last_round", "level",
                "placement", "players_eliminated", "time_eliminated", "total_damage_to_players")
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
augments_sql = '''
        INSERT INTO augments ("m_id", "puuid", "augment", "pick") 
        VALUES (%s,%s,%s,%s);'''
traits_sql = '''
        INSERT INTO traits ("m_id", "puuid", "trait_name", "num_units", "style", 
                "trait_tier_current", "trait_tier_total")
        VALUES (%s,%s,%s,%s,%s,%s,%s);'''
units_sql = '''
        INSERT INTO units ("m_id", "puuid", "unit_id", "rarity", "unit_tier", "unit_copies")
        VALUES (%s,%s,%s,%s,%s,%s);'''
items_sql = '''
        INSERT INTO items ("m_id", "puuid", "unit_id", "rarity", "unit_tier", "unit_copies", "item") 
        VALUES (%s,%s,%s,%s,%s,%s,%s);'''
