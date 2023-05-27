from termcolor import colored
from util.turn_service_off import turn_service_off
from util.turn_service_on import turn_service_on
from util.turn_galera_cluster_on import turn_galera_cluster_on
from util.test_database_proxy import test_databse_proxy


servers = [
    {
        "hostname": "database server 1",
        "db_server_ip": "192.168.178.133",
        "db_server_db_user": "root",
        "db_server_db_password": "",
        "db_server_linux_user": "ng_mariadb1",
        "db_server_linux_password": "Infra123",
        "is_primary_galera_node": True
    },
    {
        "hostname": "database server 2",
        "db_server_ip": "192.168.178.102",
        "db_server_db_user": "root",
        "db_server_db_password": "",
        "db_server_linux_user": "ngmariadb2",
        "db_server_linux_password": "Infra123",
        "is_primary_galera_node": False
    }
]

def test_database_failover(db_server):
    try:
        #Databaseverbinding testen met alle servers aan
        print(colored(f"Databaseserver:  {db_server.get('hostname')} ", "yellow"))
        print(colored("[test gestart]: Databaseverbinding testen met alle server aan", "yellow"))
        for server in servers:
            if server.get("is_primary_galera_node"):
                turn_galera_cluster_on(server_ip=server.get("db_server_ip"), user=server.get("db_server_linux_user"), password=server.get("db_server_linux_password"), sudo_password="Infra123")
            else:
                turn_service_on(server_ip=server.get("db_server_ip"), service_name="mariadb", user=server.get("db_server_linux_user"), password=server.get("db_server_linux_password"), sudo_password="Infra123")
        if test_databse_proxy():
            print(colored("[GESLAAGD]: database beschikbaar met alle servers aan!", "green"))
            if server.get("is_primary_galera_node"):
                turn_galera_cluster_on(server_ip=server.get("db_server_ip"), user=server.get("db_server_linux_user"), password=server.get("db_server_linux_password"), sudo_password="Infra123")
            else:
                turn_service_on(server_ip=server.get("db_server_ip"), service_name="mariadb", user=server.get("db_server_linux_user"), password=server.get("db_server_linux_password"), sudo_password="Infra123")
        else:
            print(colored("[gefaald]: database niet beschikbaar met alle server aan!"))
        
        
        print("\n\r")
        #testen met één(server) databaseserver uit
        print(colored(f"[test gestart]: Databaseverbinding testen met {db_server.get('hostname')} uit!", "yellow"))
        turn_service_off(server_ip=db_server.get("db_server_ip"), service_name="mariadb", user=db_server.get("db_server_linux_user"), password=db_server.get("db_server_linux_password"), sudo_password="Infra123")
        if test_databse_proxy():
            print(colored("[GESLAAGD]: database beschikbaar met één servers aan!", "green"))
        else:
            print(colored("[gefaald]: database niet beschikbaar met één server aan!"))
        
        print(colored("\n\r[INFO]: test cleanup", "blue"))
        
        if server.get("is_primary_galera_node"):
            turn_galera_cluster_on(server_ip=server.get("db_server_ip"), user=server.get("db_server_linux_user"), password=server.get("db_server_linux_password"), sudo_password="Infra123")
        else:
            turn_service_on(server_ip=server.get("db_server_ip"), service_name="mariadb", user=server.get("db_server_linux_user"), password=server.get("db_server_linux_password"), sudo_password="Infra123")        
    except Exception as e:
        print(e)
        print(colored("[Gefaald]: test gefaald!", "red"))


for db_server in servers:
    test_database_failover(db_server)
    print("\n\r post test cleanup... \n\r")
    if db_server.get("is_primary_galera_node"):
        turn_galera_cluster_on(server_ip=db_server.get("db_server_ip"), user=db_server.get("db_server_linux_user"), password=db_server.get("db_server_linux_password"), sudo_password="Infra123")
    else:
        turn_service_on(server_ip=db_server.get("db_server_ip"), service_name="mariadb", user=db_server.get("db_server_linux_user"), password=db_server.get("db_server_linux_password"), sudo_password="Infra123")