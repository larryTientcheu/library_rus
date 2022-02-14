import psycopg2
import credent as creds



## ****** LOAD PSQL DATABASE ***** ##
class PostgresManagement:
    def __init__(self):
        # Set up a connection to the postgres server.
        conn_string = "host="+ creds.PGHOST +" port="+ "5432" +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER \
            +" password="+ creds.PGPASSWORD
        conn=psycopg2.connect(conn_string)
        self.connection = conn
        self.cursor = conn.cursor()
        self.schema = 'public'
        #merci  