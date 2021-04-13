from ClientUIfoundation import Ui_MainWindow
from PyQt5 import QtWidgets
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Client
from datetime import datetime
from threading import Thread
import json
from icecream import ic
from PyQt5.QtCore import QThread


class Getter(QThread):
    def __init__(self, main_window, socket):
        super().__init__()
        self.socket = socket
        self.main_window = main_window

    def run(self):
        while True:
            # ic(self.socket)
            data = json.loads(self.socket.recv(1024).decode('utf-8'))
            self.main_window.textArea.append(f"{data['from']}:")
            self.main_window.textArea.append(data['text'])
            self.main_window.textArea.append(" ")
            # ic(data)
            # print('Работает')


class ClientWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, sock, id):
        super().__init__()
        self.sock = sock
        self.message = None

        engine = create_engine("sqlite:///database.db", echo=True)
        self.Session = sessionmaker(bind=engine)
        session = self.Session()
        # with self.Session() as session:
        client = session.query(Client).filter(Client.id == id).one()
        self.client = client
        ic(self.client)
        session.close()

        self.setupUi(self)

        self.get_login()
        self.get_contacts()

        self.sendButton.pressed.connect(self.send)

        self.getter = Getter(main_window=self, socket=self.sock)
        self.getter.start()

    def get_login(self):
        self.textBrowser.setText(self.client.login)

    def get_contacts(self):
        for friend in self.client.friends:
            ic(friend)
            self.contacts.addItem(friend.login)

    def send(self):
        self.message = self.messegeArea.toPlainText().strip()
        while "\n" in self.message:
            self.message = self.message.replace('\n', '')

        send_data = {
            "action": "sending",
            "from": f"{self.client.login}",
            "time": f"<{datetime.now()}>",
            "text": f"{self.message}"
        }
        ic(send_data)
        self.textArea.append("Вы: ")
        self.textArea.append(self.message)
        self.textArea.append(" ")
        self.sock.send(json.dumps(send_data).encode('utf-8'))
        self.message = None
        self.messegeArea.clear()
        print(send_data)

# if __name__ == '__main__':
#     app = QtWidgets.QApplication([])
#     window = ClientWindow()
#     window.show()
#     app.exec_()
