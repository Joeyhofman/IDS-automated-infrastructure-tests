from termcolor import colored
import sys

from util.turn_service_off import turn_service_off
from util.turn_service_on import turn_service_on
from util.test_web_proxy import test_web_server_proxy


servers = [
    {
        "hostname": "web server 1",
        "web_server_ip": "192.168.178.133",
        "web_server_linux_user": "ng_mariadb1",
        "web_server_linux_password": "Infra123"
    },
    {
        "hostname": "Web server 2",
        "web_server_ip": "192.168.178.102",
        "web_server_linux_user": "ngmariadb2",
        "web_server_linux_password": "Infra123"
    }
]

def test_web_server_failover(web_server):
    try:
        #Webserver verbinding testen met alle servers aan
        print(colored(f"[INFO]: test_web_server_failover met:  {web_server.get('hostname')} ", "yellow"))
        print(colored("[test gestart]: Webserver verbidning testen met alle servers aan", "yellow"))
        for server in servers:
            turn_service_on(server_ip=server.get("web_server_ip"), service_name="apache2", user=server.get("web_server_linux_user"), password=server.get("web_server_linux_password"), sudo_password="Infra123")
        if test_web_server_proxy():
            print(colored("[GESLAAGD]: database beschikbaar met alle servers aan!", "green"))
            turn_service_on(server_ip=server.get("web_server_ip"), service_name="apache2", user=server.get("web_server_linux_user"), password=server.get("web_server_linux_password"), sudo_password="Infra123")
        else:
            print(colored("[gefaald]: database niet beschikbaar met alle server aan!"))
            sys.exit()
        
        
        print("\n\r")
        #testen met één(web server) webserver uit
        print(colored(f"[test gestart]: Databaseverbinding testen met {web_server.get('hostname')} uit!", "yellow"))
        turn_service_off(server_ip=web_server.get("web_server_ip"), service_name="apache2", user=web_server.get("web_server_linux_user"), password=web_server.get("web_server_linux_password"), sudo_password="Infra123")
        if test_web_server_proxy():
            print(colored("[GESLAAGD]: database beschikbaar met één servers aan!", "green"))
        else:
            print(colored("[gefaald]: database niet beschikbaar met één server aan!"))
        
        print(colored("\n\r[INFO]: test cleanup", "blue"))
        turn_service_on(server_ip=web_server.get("web_server_ip"), service_name="apache2", user=web_server.get("web_server_linux_user"), password=web_server.get("web_server_linux_password"), sudo_password="Infra123")
        
          
    except Exception as e:
        print(e)
        print(colored("[Gefaald]: test gefaald!", "red"))


for web_server in servers:
    test_web_server_failover(web_server)