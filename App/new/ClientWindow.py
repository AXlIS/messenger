from ClientUIfoundation import Ui_MainWindow
from PyQt5 import QtWidgets
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import ClientStorage
from datetime import datetime
import json
from icecream import ic
from PyQt5.QtCore import QThread, QEvent
from database import MongoStorage


class Getter(QThread):
    def __init__(self, main_window, socket):
        """
        :param main_window: UI object
        :type main_window: :class:`ClientWindow.ClientWindow`
        :param socket: Socket
        :type socket: :class:`socket.socket`
        """
        super().__init__()
        self.socket = socket
        self.main_window = main_window
        self.mongo = MongoStorage()

    def run(self):
        """Method for reading, processing and displaying messages"""
        while True:
            data = json.loads(self.socket.recv(1024).decode('utf-8'))
            if data["from"] == self.main_window.chat_with.toPlainText():
                self.main_window.textArea.append(f"{data['from']}:")
                self.main_window.textArea.append(data['text'])
                self.main_window.textArea.append(" ")


class ClientWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """User interface and logic"""

    def __init__(self, sock, id):
        super().__init__()
        self.sock = sock
        self.message = None

        self.mongo = MongoStorage()

        engine = create_engine("sqlite:///database.db", echo=True)
        self.Session = sessionmaker(bind=engine)
        with self.Session() as session:
            client_storage = ClientStorage(session)
            self.client = client_storage.find(id)
            self.friends = client_storage.friends(id)

        self.sender = self.friends[0].login if len(self.friends) > 0 else None

        self.setupUi(self)

        self.get_login()
        self.get_contacts()
        self.load_messages()

        self.sendButton.pressed.connect(self.send)
        self.contacts.itemClicked.connect(self.current_item)

        self.getter = Getter(main_window=self, socket=self.sock)
        self.getter.start()

    def load_messages(self):
        for message in self.mongo.get_messages(self.client.login, self.sender):
            self.message_write(message["text"], message["from"])

    def get_login(self):
        """Rendering the login on the page"""
        self.textBrowser.setText(self.client.login)
        self.chat_with.setText(self.sender)

    def get_contacts(self):
        """Rendering the list of contacts on the page"""
        for friend in self.friends:
            self.contacts.addItem(friend.login)

    def event(self, e):
        if e.type() == QEvent.KeyPress:
            if e.key() == 16777220:
                self.send()

        return super().event(e)

    def send(self):
        """Sending messages"""
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
            self.mongo.add(send_data)
            self.message_write(self.message, self.client.login)

    def message_write(self, message, sender):
        """Adding messages to the page"""
        self.textArea.append(f'{sender}:')
        self.textArea.append(message)
        self.textArea.append(" ")
        self.message = None
        self.messageArea.clear()

    def current_item(self):
        """Selecting a contact"""
        current_contact = self.contacts.currentItem()
        if current_contact.text() != self.sender:
            self.textArea.clear()
        if current_contact.text != 'Контакты':
            self.sender = current_contact.text()
            self.chat_with.setText(self.sender)
            self.load_messages()
            ic(self.sender)
