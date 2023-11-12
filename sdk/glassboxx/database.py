import importlib
import re

# Global configuration object
global_config = {
    'api_key': 'your_api_key_here',
    'db_connection': None
}

def create_connection(db_type, connection_string):
    """ Create a database connection based on the database type """
    conn = None
    try:
        if db_type == 'postgresql':
            psycopg2 = importlib.import_module('psycopg2')
            conn = psycopg2.connect(connection_string)
        elif db_type == 'mysql':
            mysql = importlib.import_module('mysql.connector')
            conn = mysql.connector.connect(connection_string)
        elif db_type == 'sqlite':
            sqlite3 = importlib.import_module('sqlite3')
            conn = sqlite3.connect(connection_string)
    except Exception as e:
        print(f"Database connection error: {e}")
    
    return conn

def create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")

def parse_db_type(connection_string):
    """ Parse the connection string to identify the database type """
    if connection_string.startswith('postgres://') or connection_string.startswith('postgresql://'):
        return 'postgresql'
    elif connection_string.startswith('mysql://'):
        return 'mysql'
    elif connection_string.startswith('sqlite:///'):
        return 'sqlite'
    else:
        raise ValueError("Unsupported database type")

def log_tables_and_contents(conn, db_type):
    """ Logs the tables and their contents """
    cur = conn.cursor()

    # Query to list tables varies by database type
    list_tables_query = ""
    if db_type == 'postgresql' or db_type == 'mysql':
        list_tables_query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    elif db_type == 'sqlite':
        list_tables_query = "SELECT name FROM sqlite_master WHERE type='table';"

    # List tables
    cur.execute(list_tables_query)
    tables = cur.fetchall()
    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")

        # Query to print table contents
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        for row in rows:
            print(row)
            
def init_db(connection_string):
    """
    Initializes the database connection.
    :param connection_string: The database connection string.
    """
    if connection_string:
        # Parse the database type from the connection string
        db_type = parse_db_type(connection_string)

        # Establish a database connection
        conn = create_connection(db_type, connection_string)

        if conn is not None:
            # SQL statements for creating your tables
            create_logs_table = """
                CREATE TABLE IF NOT EXISTS glassboxx__logs (
                    id SERIAL PRIMARY KEY,
                    request_id TEXT NOT NULL,
                    stage TEXT,  -- e.g., 'raw_input', 'engineered_prompt', 'tokenized', final_output etc.
                    log_data TEXT,  -- Data relevant to the specific stage
                    timestamp TIMESTAMP
                );
            """

            create_explanations_table = """
                CREATE TABLE IF NOT EXISTS glassboxx__explanations (
                    id SERIAL PRIMARY KEY,
                    request_id TEXT NOT NULL,
                    explanation_output TEXT,
                    explanation_type TEXT,
                    timestamp TIMESTAMP
                );
            """

            create_insights_table = """
                CREATE TABLE IF NOT EXISTS glassboxx__insights (
                    id SERIAL PRIMARY KEY
                    -- Define the fields based on your requirements
                );
            """

            # Create tables
            create_table(conn, create_logs_table)
            create_table(conn, create_explanations_table)
            create_table(conn, create_insights_table)

            # Log tables and their contents
            log_tables_and_contents(conn, db_type)

            # Store the connection in the global config
            global_config['db_connection'] = conn
        else:
            print("Error! Cannot create the database connection.")
    else:
        # TODO: Implement the logic to send data to glassboxx servers using `api_key`
        pass
