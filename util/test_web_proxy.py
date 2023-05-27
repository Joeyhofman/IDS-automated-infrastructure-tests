import requests
from termcolor import colored

proxy_url = "http://192.168.178.133/"

def test_web_server_proxy():
    print(colored(f"[INFO]: Verbinding maken met web server proxy({proxy_url})...", "yellow"))
    response = requests.get(proxy_url)
    return response.status_code == 200