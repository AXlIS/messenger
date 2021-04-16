from ClientUIfoundation import Ui_MainWindow
from PyQt5 import QtWidgets
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import ClientStorage
from datetime import datetime
import json
from icecream import ic
from PyQt5.QtCore import QThread, QEvent


class Getter(QThread):
    def __init__(self, main_window, socket):
        super().__init__()
        self.socket = socket
        self.main_window = main_window

    def run(self):
        while True:
            data = json.loads(self.socket.recv(1024).decode('utf-8'))
            if data["from"] == self.main_window.chat_with.toPlainText():
                self.main_window.textArea.append(f"{data['from']}:")
                self.main_window.textArea.append(data['text'])
                self.main_window.textArea.append(" ")


class ClientWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, sock, id):
        super().__init__()
        self.sock = sock
        self.message = None

        engine = create_engine("sqlite:///database.db", echo=True)
        self.Session = sessionmaker(bind=engine)
        with self.Session() as session:
            client_storage = ClientStorage(session)
            self.client = client_storage.find(id)
            self.friends = client_storage.friends(id)
            # ic(self.client)
        self.sender = self.friends[0].login if len(self.friends) > 0 else None

        self.setupUi(self)

        self.get_login()
        self.get_contacts()

        self.sendButton.pressed.connect(self.send)
        self.contacts.itemClicked.connect(self.current_item)

        self.getter = Getter(main_window=self, socket=self.sock)
        self.getter.start()

    def get_login(self):
        self.textBrowser.setText(self.client.login)
        self.chat_with.setText(self.sender)

    def get_contacts(self):
        for friend in self.friends:
            self.contacts.addItem(friend.login)

    def event(self, e):
        if e.type() == QEvent.KeyPress:
            if e.key() == 16777220:
                self.send()

        return super().event(e)

    def send(self):
        self.message = self.messageArea.text().strip()
        if self.message:
            while "\n" in self.message:
                self.message = self.message.replace('\n', '')

            send_data = {
                "action": "sending",
                'to': f'{self.sender}',
                "from": f"{self.client.login}",
                "time": f"<{datetime.now()}>",
                "text": f"{self.message}"
            }
            self.sock.send(json.dumps(send_data).encode('utf-8'))
            self.message_write()
            ic(send_data)

    def message_write(self):
        self.textArea.append("Вы: ")
        self.textArea.append(self.message)
        self.textArea.append(" ")
        self.message = None
        self.messageArea.clear()

    def current_item(self):
        current_contact = self.contacts.currentItem()
        if current_contact.text() != self.sender:
            self.textArea.clear()
        self.sender = current_contact.text()
        self.chat_with.setText(self.sender)
        ic(self.sender)

# if __name__ == '__main__':
#     app = QtWidgets.QApplication([])
#     window = ClientWindow()
#     window.show()
#     app.exec_()
