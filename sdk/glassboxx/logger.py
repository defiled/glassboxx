from datetime import datetime
from .utils import RequestIDManager
from .config import get_config

def log(data, log_type):
    """
    Logs the given data with the specified type to the database, associating it with a unique request ID.

    :param data: The data to be logged.
    :param log_type: The type of the log (e.g., 'raw', 'processed', 'output', 'tokenized').
    """
    request_id = RequestIDManager.get_request_id()
    data_str = str(data)
    timestamp = datetime.now()

    # SQL query to insert the log entry
    insert_query = """INSERT INTO glassboxx__logs (request_id, stage, log_data, timestamp)
                      VALUES (%s, %s, %s, %s)"""

    # Fetch the database connection from the global configuration
    conn = get_config('db_connection')
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(insert_query, (request_id, log_type, data_str, timestamp))
                conn.commit()
        except Exception as e:
            print(f"Error logging data: {e}")
    else:
        print("Database connection not established.")

    print(f"Logged data: {data_str}, Type: {log_type}, Request ID: {request_id}")