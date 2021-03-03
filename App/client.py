import click
import json
from time import time
from socket import socket, AF_INET, SOCK_STREAM


# @click.command()
# @click.option("--port", default=7777)
# @click.option("--addr", default='localhost')
def client(port, addr):
    send_data = {
        "action": "authenticate",
        "time": f"< {int(time())} >",
        "user": {
            "account_name": "C0deMaver1ck",
            "password": "CorrectHorseBatterStaple"
        }
    }
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((addr, port))
        s.send(json.dumps(send_data).encode('ascii'))
        data = s.recv(1024)
        return json.loads(data.decode('ascii'))


if __name__ == '__main__':
    client()
