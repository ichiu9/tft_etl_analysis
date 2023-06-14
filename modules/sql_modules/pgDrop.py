import requests
import psycopg2
from modules.psycop_modules.createConnection import *

def drop_tables(cursor, connection):
    commands = """DROP TABLE IF EXISTS matches CASCADE;
                  DROP TABLE IF EXISTS players_in_match CASCADE;
                  DROP TABLE IF EXISTS player_stats;
                  DROP TABLE IF EXISTS traits;
                  DROP TABLE IF EXISTS units CASCADE;
                  DROP TABLE IF EXISTS augments;
                  DROP TABLE IF EXISTS items;
               """
    try:
        cursor.execute(commands)
        print("Dropped Tables: [matches, player_stats, traits, augments, units, players_in_match]")
    except psycopg2.Error as e:
        print("Error: Failed to drop tables: [matches, player_stats, traits, augments, units, players_in_match]")
        print(e)