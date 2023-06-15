import psycopg2

# Create connection to Database
def create_connection(host, dbname, user, password):
    print(host, dbname, user, password)
    try:
        conn = psycopg2.connect("host={} dbname={} user={} password={}".format(host, dbname, user, password))
        conn.set_session(autocommit=True)
    except psycopg2.Error as e:
        print("Error: Could not make connection to the Postgres database")
        print(e)

    #Use the connection to get a cursor that can be used to execute queries.
    try:
        cur = conn.cursor()
    except psycopg2.Error as e:
        print("Error: Could not get cursor to the Database")
        print(e) 

    return conn, cur