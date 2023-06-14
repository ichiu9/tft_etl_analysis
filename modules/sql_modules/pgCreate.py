import requests
import psycopg2 
from modules.psycop_modules.createConnection import *

def create_tables(cursor, connection):
    commands = '''
    CREATE TABLE matches(
        m_id VARCHAR(20) NOT NULL,
        m_datetime BIGINT,
        m_length DECIMAL,
        PRIMARY KEY(m_id)
    );
    
    CREATE TABLE players_in_match(
        m_id VARCHAR(20) NOT NULL,
        puuid VARCHAR(100) NOT NULL,
        PRIMARY KEY(m_id, puuid),
        FOREIGN KEY (m_id) REFERENCES matches (m_id)
    );
    
    CREATE TABLE player_stats(
        m_id VARCHAR(20) NOT NULL,
        puuid VARCHAR(100) NOT NULL,
        gold_left INT, 
        last_round INT,
        level INT,
        placement INT,
        players_eliminated INT,
        time_eliminated FLOAT,
        total_damage_to_players INT,
        FOREIGN KEY (m_id, puuid) REFERENCES players_in_match (m_id, puuid),
        PRIMARY KEY(m_id, puuid)
    );
    
    CREATE TABLE traits(
        m_id VARCHAR(20) NOT NULL,
        puuid VARCHAR(100) NOT NULL,
        trait_name VARCHAR(100) NOT NULL,
        num_units INT,
        style INT,
        trait_tier_current INT,
        trait_tier_total INT,
        FOREIGN KEY (m_id, puuid) REFERENCES players_in_match (m_id, puuid),
        PRIMARY KEY(m_id, puuid, trait_name)
    );
    
    CREATE TABLE augments(
        m_id VARCHAR(20) NOT NULL,
        puuid VARCHAR(100) NOT NULL,
        augment VARCHAR(100) NOT NULL,
        pick INT,
        FOREIGN KEY (m_id, puuid) REFERENCES players_in_match (m_id, puuid),
        PRIMARY KEY(m_id, puuid, augment)
    );
    
    CREATE TABLE units(
        m_id VARCHAR(20) NOT NULL,
        puuid VARCHAR(100) NOT NULL,
        unit_id VARCHAR(100) NOT NULL,
        rarity INT,
        unit_tier INT,
        unit_copies INT,
        PRIMARY KEY(m_id, puuid, unit_id, rarity, unit_tier, unit_copies),
        FOREIGN KEY (m_id, puuid) REFERENCES players_in_match (m_id, puuid)
    );

    CREATE TABLE items(
        m_id VARCHAR(20) NOT NULL,
        puuid VARCHAR(100) NOT NULL,
        unit_id VARCHAR(100) NOT NULL,
        rarity INT,
        unit_tier INT,
        unit_copies INT,
        item VARCHAR(100) NOT NULL,
        FOREIGN KEY (m_id, puuid) REFERENCES players_in_match (m_id, puuid),
        FOREIGN KEY (m_id, puuid, unit_id, rarity, unit_tier, unit_copies) REFERENCES units (m_id, puuid, unit_id, rarity, unit_tier, unit_copies)
    );
    '''
    
    try:
        cursor.execute(commands)
        print("Created tables: [matches, player_match_stats, player_match_traits, player_match_units]")
    except psycopg2.Error as e:
        print("Error: Failed to create tables: [matches, player_match_stats, player_match_traits, player_match_units]")
        print(e)

