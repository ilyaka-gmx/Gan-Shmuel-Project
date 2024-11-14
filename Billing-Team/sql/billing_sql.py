from orm import Table, get_table
import os

db_config = {
    'host': os.environ.get("DB_HOST", "localhost"),
    'port': int(os.environ.get("DB_PORT", 3306)),
    'user': os.environ.get("DB_USER", "root"),
    'password': os.environ.get("MYSQL_ROOT_PASSWORD", "123456"),
    'database': os.environ.get("MYSQL_DATABASE", "billdb"),
}

def db_connection():
    Table.connect(config_dict=db_config)

# Connect to the database and create tables if needed
def providers():
    db_connection()
    Providers = get_table('Provider')
    return Providers

def rates():
    db_connection()
    Rates = get_table('rates')
    return Rates

def trucks():
    db_connection()
    Trucks = get_table('trucks')
    return Trucks

