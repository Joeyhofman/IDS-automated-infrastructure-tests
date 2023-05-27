import paramiko
from termcolor import colored

def turn_service_on(server_ip, service_name, user, password, sudo_password):
    try:
        print(colored(f"[INFO]: {service_name} inschakelen({server_ip})...", "yellow"))
        command_result = []
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(server_ip, username=user, password=password)
        stdin, stdout, stderr = client.exec_command(f"sudo -S service {service_name} start")
        stdin.write(sudo_password + "\n")
        stdin.flush()
        for line in stdout:
            print(line)
            command_result.append(line)

        if not command_result:
            print(colored(f"[INFO]: {service_name} is ingeschakeld!".capitalize(), "green"))
            return True
        else:
            print(colored(f"[WARNING]: Kon {service_name} is uitschakelen!".capitalize(), "red"))
            return False
    except IndexError as ie:
        print(ie)
        return False
    except Exception as e:
        print(e)
        return False
    finally:
        client.close()