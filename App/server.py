import click
import json
from socket import socket, AF_INET, SOCK_STREAM
from time import time
from contextlib import closing


@click.command()
@click.option("--port", default=7777)
@click.option("--addr", default='')
def server(port, addr):
    send_data = '{' + f'"action": "probe", "time": <{int(time())}>,' + '}'
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((addr, port))
        s.listen()

        while True:
            client, addr = s.accept()

            with closing(client) as c:
                data = client.recv(1024)
                print(f"{json.loads(data.decode('ascii'))}, Клиент: {addr}")
                client.send(json.dumps(send_data).encode('ascii'))


if __name__ == '__main__':
    server()
