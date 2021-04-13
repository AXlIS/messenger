import json
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM
from icecream import ic
from threading import Thread


class ClientItem:

    def __init__(self, port=7777, addr='localhost'):
        self.port = port
        self.addr = addr

    def send(self):
        while True:
            send_data = {
                "action": "send_message",
                "message": f"Ваш собеседник: {input()}",
            }
            self.sock.send(json.dumps(send_data).encode('utf-8'))

            if send_data['message'] == 'b':
                break

    def get(self):
        while True:
            data = self.sock.recv(1024).decode('utf-8')
            print(json.loads(data)["message"])

    def run(self):
        while True:
            sender = Thread(target=self.send)
            g = Thread(target=self.get)
            sender.start()
            g.start()
            sender.join()


if __name__ == '__main__':
    client = ClientItem()
