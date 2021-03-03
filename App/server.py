import click
import json
from socket import socket, AF_INET, SOCK_STREAM
from time import time
from contextlib import closing


@click.command()
@click.option("--port", default=7777)
@click.option("--addr", default='')
def server(port, addr):
    send_data = {
        "action": "probe",
        "time": f"<{int(time()) // 10000}>"
    }
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((addr, port))
        s.listen()
        while True:
            client, addr = s.accept()
            with closing(client) as c:
                data = json.loads(client.recv(100000).decode('utf-8'))
                print(f"{data}, Клиент: {addr}, {type(data)}")
                if "action" in data and data["action"] == "authenticate":
                    client.send(json.dumps(send_data).encode('ascii'))


if __name__ == '__main__':
    server()
