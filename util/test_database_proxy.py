from mysql.connector import connection
from termcolor import colored

db_proxy_ip = "192.168.178.102"
db_proxy_db_user = "root"
db_proxy_db_password = ""

def test_databse_proxy():
    print(colored(f"Verbinding maken met database proxy({db_proxy_ip})...", "yellow"))
    cnx = connection.MySQLConnection(user=db_proxy_db_user, password=db_proxy_db_password,
                                 host=db_proxy_ip,
                                 database='nerdygadgets')
    return cnx