from orm import Table, get_table
import os

db_config = {
    'host': os.environ.get("DB_HOST", "host.docker.internal"),
    'port': int(os.environ.get("DB_PORT", 3306)),
    'user': os.environ.get("DB_USER", "root"),
    'password': os.environ.get("MYSQL_ROOT_PASSWORD", ""),
    'database': os.environ.get("MYSQL_DATABASE", "billdb"),
}

# Connect to the database and create tables if needed
Table.connect(config_dict=db_config)
Providers = get_table('Provider')
Rates = get_table('Rates')
Trucks = get_table('Trucks')

#test function needs to remove after first API will work with the BD
def test_function():
    new_provider = Providers.create(name='dany')
    provider = Providers.find(id=10001)
    print(provider.name)

if __name__ == '__main__':
    test_function()
