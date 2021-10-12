# Ripped straight from https://www.postgresqltutorial.com/postgresql-python/connect/

from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    # Create parser
    parser = ConfigParser()
    # Read config file
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in {filename}')

    return db
