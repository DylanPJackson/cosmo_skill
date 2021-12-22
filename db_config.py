# Ripped straight from https://www.postgresqltutorial.com/postgresql-python/connect/
import os

def config():
    db = {}
    try:
        host = os.environ["HOST"]
        database = os.environ["DATABASE"]
        user = os.environ["USER"]
        password = os.environ["PASSWORD"]
        db['host'] = host
        db['database'] = database
        db['user'] = user
        db['password'] = password
    except KeyError as err:
        print(f"KeyError, {err}") 
    finally:
        return db
