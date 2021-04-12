from LoginUIfoundation import Ui_MainWindow
from PyQt5 import QtWidgets
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
import json
from icecream import ic
from ClientUI import ClientWindow


class LoginWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, port, addr):
        super().__init__()
        self.port = port
        self.addr = addr

        self.setupUi(self)

        self.singIn.pressed.connect(self.authenticate)

    def authenticate(self):
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect((self.addr, self.port))
            send_data = {
                "action": "authenticate",
                "time": f"<{datetime.now()}>",
                "login": self.login.text(),
                "password": self.password.text()
            }
            self.connect_socket(self.port, self.addr)
            self.sock.send(json.dumps(send_data).encode('utf-8'))
            data = json.loads(self.sock.recv(1024).decode('utf-8'))
            ic(data)
            if data["response"] == 202:
                print('гуд')
            elif data["response"] == 400:
                print('Что то пожло не так..')
            # self.sock.close()
            # self.login.clear()
            # self.password.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = LoginWindow(7777, 'localhost')
    window.show()
    app.exec_()
