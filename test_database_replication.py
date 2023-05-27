from mysql.connector import connection
from termcolor import colored

servers = [
    {
        "hostname": "database server 1",
        "db_server_ip": "192.168.178.133",
        "db_server_db_user": "root",
        "db_server_db_password": "",
    },
    {
        "hostname": "database server 2",
        "db_server_ip": "192.168.178.102",
        "db_server_db_user": "root",
        "db_server_db_password": "",
    }
]

def test_database_replication_for_servers():
    try:
        db1_connection = connection.MySQLConnection(user=servers[0].get("db_server_db_user"), password=servers[0].get("db_server_db_password"),
                                    host=servers[0].get("db_server_ip"),
                                    database='nerdygadgets')
        db1_cursor = db1_connection.cursor()
        
        db2_connection = connection.MySQLConnection(user=servers[1].get("db_server_db_user"), password=servers[1].get("db_server_db_password"),
                                    host=servers[1].get("db_server_ip"),
                                    database='nerdygadgets')
        db2_cursor = db2_connection.cursor()
        
        print(colored(f"[INFO]: Aanmaken replication_test databas op: {servers[0].get('hostname')}...", "yellow"))
        db1_cursor.execute("CREATE DATABASE IF NOT EXISTS replication_test")
        
        print(colored(f"[INFO]: Kijken of de replication_test database op: {servers[1].get('hostname')} bestaat...", "yellow"))
        db2_cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'replication_test'")
        record = db2_cursor.fetchone()
        
        if record and record[0] == "replication_test":
            print(colored(f"[GESLAAGD]: database replicatie voor {servers[0].get('hostname')} geslaagd!", "green"))
        else:
            print(colored(f"[GEFAALD]: database replicatie voor {servers[0].get('hostname')} GEFAALD!", "red"))
        
        
        print(colored(f"[INFO]: test cleanup...", "blue"))
        db1_cursor.execute("DROP DATABASE IF EXISTS replication_test")
        


        print(colored(f"[INFO]: Aanmaken replication_test databas op: {servers[1].get('hostname')}", "yellow"))
        db2_cursor.execute("CREATE DATABASE IF NOT EXISTS replication_test")
        
        print(colored(f"[INFO]: Kijken of de replication_test database op: {servers[0].get('hostname')} bestaat...", "yellow"))
        db1_cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'replication_test'")
        record = db1_cursor.fetchone()
        
        if record and record[0] == "replication_test":
            print(colored(f"[GESLAAGD]: database replicatie voor {servers[1].get('hostname')} geslaagd!", "green"))
        else:
            print(colored(f"[GEFAALD]: database replicatie voor {servers[1].get('hostname')} GEFAALD!", "red"))
        
        print(colored(f"[INFO]: test cleanup...", "blue"))
        db2_cursor.execute("DROP DATABASE IF EXISTS replication_test")
        
        
    except Exception as e:
        print(e)
        db1_connection = None;
        db2_connection = None;
        print(colored("[GEFAALD]: test gefaald!", "red"))
    finally:
        if db1_connection: db1_connection.close()
        if db2_connection: db2_connection.close()
    
    

test_database_replication_for_servers()
    