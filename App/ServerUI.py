# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ServerUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from PyQt5 import QtCore, QtGui, QtWidgets
from ServerUIfoundation import Ui_MainWindow
from database import Client, ClientHistory
from PyQt5 import QtGui


class Window(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        engine = create_engine("sqlite:///database.db", echo=True)
        self.Session = sessionmaker(bind=engine)
        self.setupUi(self)

        self.load_users()
        self.load_history()

        self.usersAddButton.pressed.connect(self.add_user)
        self.usersDeleteButton.pressed.connect(self.delete_message)

    def load_users(self):
        with self.Session() as session:
            for user in session.query(Client).all():
                rowPosition = self.usersTable.rowCount()
                self.usersTable.insertRow(rowPosition)
                self.usersTable.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(f"{user.id}"))
                self.usersTable.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(f"{user.login}"))
                self.usersTable.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(f"{user.password}"))

    def load_history(self):
        with self.Session() as session:
            for history in session.query(ClientHistory).all():
                rowPosition = self.usersStateTable.rowCount()
                self.usersStateTable.insertRow(rowPosition)
                self.usersStateTable.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(f"{history.client_id}"))
                self.usersStateTable.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(f"{history.ip}"))
                self.usersStateTable.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(f"{history.time}"))
                self.usersStateTable.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(f"{history.status}"))

    def add_user(self):
        print('add')

    def delete_message(self):
        print('delete')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Window()
    window.show()
    app.exec_()