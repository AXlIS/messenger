from ClientUIfoundation import Ui_MainWindow
from PyQt5 import QtWidgets
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
import json
from icecream import ic


class ClientWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock

        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = ClientWindow()
    window.show()
    app.exec_()
