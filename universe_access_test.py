import psycopg2
from db_config import config

def connect():
    """Connect to PSQL db and execute command."""

    conn = None

    g_id = 1
    explanation = "script test"
    time_spent = "3 minutes"
    date = "2021-10-14"
    sql = f"INSERT INTO goal_log VALUES ({g_id},'{explanation}','{time_spent}','{date}')"
    try:
        # Read connection parameters
        print("Reading in connection parameters")
        params = config()

        # Connect to db
        print("Connecting to db")
        conn = psycopg2.connect(**params)
        print("Connected")

        # Create cursor
        print("Opening cursor")
        cur = conn.cursor()

        print("Sending message")
        cur.execute(sql)

        print("Commiting message")
        conn.commit()

        print("Closing cursor") 
        cur.close()
    except (Exception, psycopg2.DatabaseError) as err:
        print(err)
    finally:
        if conn is not None:
            print("Closing db connection")
            conn.close()
            print("Connection closed")

if __name__ == "__main__":
    connect()
