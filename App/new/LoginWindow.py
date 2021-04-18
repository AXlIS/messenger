import json
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM
from icecream import ic
from LoginUIfoundation import Ui_MainWindow
from ClientWindow import ClientWindow
from PyQt5 import QtWidgets


class LoginWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """User interface and authorization logic"""

    def __init__(self, port=7777, addr='localhost'):
        """
        :param port: Port
        :type port: int
        :param addr: Address
        :type addr: str
        """
        super().__init__()
        self.port = port
        self.addr = addr
        # self.connect_socket()

        self.setupUi(self)

        self.singIn.pressed.connect(self.authenticate)

        self.client_window = None

    def connect_socket(self):
        """Socket connection"""
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.addr, self.port))

    def authenticate(self):
        """Sending user authorization data"""
        send_data = {
            "action": "authenticate",
            "time": f"<{datetime.now()}>",
            "login": f"{self.login.text()}",
            "password": f"{self.password.text()}"
        }
        self.connect_socket()
        self.sock.send(json.dumps(send_data).encode('utf-8'))
        data = json.loads(self.sock.recv(1024).decode('utf-8'))
        ic(data)
        if data["response"] == 202:
            self.close()
            self.client_window = ClientWindow(self.sock, data["user_id"])
            self.client_window.show()
        elif data["response"] == 400:
            print('Что то пожло не так..')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = LoginWindow()
    window.show()
    app.exec_()
