import psycopg2

# Create connection to Database
def create_connection(dbname, user, password):
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname={} user={} password={}".format(dbname, user, password))
    except psycopg2.Error as e:
        print("Error: Could not make connection to the Postgres database")
        print(e)
   
    # Set automatic commit to be true so that each action is committed without having a call conn.commit() after each command
    conn.set_session(autocommit=True)

    #Use the connection to get a cursor that can be used to execute queries.
    try:
        cur = conn.cursor()
    except psycopg2.Error as e:
        print("Error: Could not get cursor to the Database")
        print(e) 

    return conn, cur