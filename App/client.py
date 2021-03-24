import click
import json
from time import time
from socket import socket, AF_INET, SOCK_STREAM
from chat.client_socket import ClientSocket
import logging
import loggers.client_log_config
from logger_decorator import log_start
from threading import Thread

logger = logging.getLogger('client.main')


def send(s, send_data):
    while True:
        s.send(json.dumps(send_data).encode('utf-8'))
        send_data = {
            "action": "send_message",
            "message": f"Ваш собеседник: {input()}",
        }
        if send_data['message'] == 'b':
            break


def get(s):
    while True:
        data = s.recv(1024).decode('utf-8')
        print(json.loads(data)["message"])


@click.command()
@click.option("--port", default=7777)
@click.option("--addr", default='localhost')
# @click.option("--send", is_flag=True)
@log_start
def client(port, addr):
    send_data = {
        "action": "authenticate",
        "time": f"< {int(time())} >",
    }
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((addr, port))
        while True:
            sender = Thread(target=send, args=(s, send_data, ))
            g = Thread(target=get, args=(s,))
            sender.start()
            g.start()
            sender.join()
            # if send:
            #     while True:
            #         s.send(json.dumps(send_data).encode('utf-8'))
            #         send_data = {
            #             "action": "authenticate",
            #             "message": f"{input('Ваше сообщение: ')}",
            #         }
            #         if send_data['message'] == 'b':
            #             break
            #     break
            # else:
            #     data = s.recv(1024).decode('utf-8')
            #     print(json.loads(data)["message"])
            # logger.info(f"Message: {json.loads(data.decode('utf-8'))}")
            # print(json.loads(data.decode('utf-8')))

        # @click.command()
        # @click.option("--port", default=7777)
        # @click.option("--addr", default='localhost')
        # def main(port, addr):
        #     with socket(AF_INET, SOCK_STREAM) as s:
        #         s.connect((addr, port))
        #         client_socket = ClientSocket(s)


if __name__ == '__main__':
    client()
