from icecream import ic
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
import json
from threading import Thread
from ClientUI import ClientWindow
from LoginUI import LoginWindow
from PyQt5 import QtWidgets


class ClientItem:

    def __init__(self, addr='localhost', port=7777):
        self.addr = addr
        self.port = port
        self.authenticate()
        # app = QtWidgets.QApplication([])
        # window = LoginWindow(self.port, self.addr)
        # window.show()
        # app.exec_()

    def connect_socket(self, port, addr):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((addr, port))

    def authenticate(self):
        while True:
            with socket(AF_INET, SOCK_STREAM) as sock:
                sock.connect((self.addr, self.port))
                send_data = {
                    "action": "authenticate",
                    "time": f"<{datetime.now()}>",
                    "login": f"{input('Введите логин: ')}",
                    "password": f"{input('Введите пароль: ')}"
                }
                self.connect_socket(self.port, self.addr)
                self.sock.send(json.dumps(send_data).encode('utf-8'))
                data = json.loads(self.sock.recv(1024).decode('utf-8'))
                ic(data)
                if data["response"] == 202:
                    print("гуд")
                    self.run()
                elif data["response"] == 400:
                    print('Что то пожло не так..')
                    self.sock.close()

    def send(self):
        while True:
            send_data = {
                "action": "send_message",
                "message": f"{input()}",
            }
            if send_data['message'] == 'b':
                break

            self.sock.send(json.dumps(send_data).encode('utf-8'))

    def get(self):
        while True:
            data = json.loads(self.sock.recv(1024).decode('utf-8'))
            print(f"Ваш собеседник: {data['message']}")

    def run(self):
        sender = Thread(target=self.send, args=())
        g = Thread(target=self.get, args=())
        sender.start()
        g.start()
        sender.join()


if __name__ == '__main__':
    client = ClientItem()
