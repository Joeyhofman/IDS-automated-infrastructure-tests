from termcolor import colored

print(colored("\n\r==========TEST_WEB_SERVER_FAILOVER==========\n\r"))
import test_web_server_failover
print(colored("\n\r==========TEST_DATABASE_FAILOVER==========\n\r"))
import test_database_failover
print(colored("\n\r==========TEST_WEB_DATABASE_REPLICATIE==========\n\r"))
import test_database_replication
