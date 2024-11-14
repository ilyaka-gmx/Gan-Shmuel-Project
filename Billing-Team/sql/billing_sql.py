from orm import Table, get_table
import os

db_config = {
    'host': os.environ.get("DB_HOST", "host.docker.internal"),
    'port': int(os.environ.get("DB_PORT", 3306)),
    'user': os.environ.get("DB_USER", "root"),
    'password': os.environ.get("MYSQL_ROOT_PASSWORD", "123456"),
    'database': os.environ.get("MYSQL_DATABASE", "billdb"),
}

# Connect to the database and create tables if needed
Table.connect(config_dict=db_config)
Providers = get_table('Provider')
Rates = get_table('Rates')
Trucks = get_table('Trucks')
# def init_db_tables():
#     with mysql.connector.connect(**db_config) as conn:
#         with conn.cursor() as cursor:
#             cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(db_config['database']))

def test_function():
    new_provider = Providers.create(name='test')
    print(new_provider)

if __name__ == '__main__':
    # Initialize database
    # init_db()
    test_function()
