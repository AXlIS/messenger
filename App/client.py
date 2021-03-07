import click
import json
from time import time
from socket import socket, AF_INET, SOCK_STREAM
from chat.client_socket import ClientSocket
import logging
import log.client_log_config

logger = logging.getLogger('client.main')


@click.command()
@click.option("--port", default=7777)
@click.option("--addr", default='localhost')
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
        logger.info(f"Message: {json.loads(data.decode('ascii'))}")


# @click.command()
# @click.option("--port", default=7777)
# @click.option("--addr", default='localhost')
# def main(port, addr):
#     with socket(AF_INET, SOCK_STREAM) as s:
#         s.connect((addr, port))
#         client_socket = ClientSocket(s)


if __name__ == '__main__':
    client()
