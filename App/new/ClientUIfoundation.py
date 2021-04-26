# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClientUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        MainWindow.setMinimumSize(QtCore.QSize(900, 600))
        MainWindow.setMaximumSize(QtCore.QSize(900, 600))
        font = QtGui.QFont()
        font.setPointSize(14)
        MainWindow.setFont(font)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Title = QtWidgets.QLabel(self.centralwidget)
        self.Title.setGeometry(QtCore.QRect(360, 10, 171, 81))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei Light")
        font.setPointSize(24)
        self.Title.setFont(font)
        self.Title.setObjectName("Title")
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(810, 510, 61, 41))
        self.sendButton.setObjectName("sendButton")
        self.contactsArea = QtWidgets.QScrollArea(self.centralwidget)
        self.contactsArea.setGeometry(QtCore.QRect(20, 100, 231, 451))
        self.contactsArea.setWidgetResizable(True)
        self.contactsArea.setObjectName("contactsArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 229, 449))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.contacts = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.contacts.setLineWidth(4)
        self.contacts.setObjectName("contacts")
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.contacts.addItem(item)
        self.verticalLayout.addWidget(self.contacts)
        self.contactsArea.setWidget(self.scrollAreaWidgetContents)
        self.textArea = QtWidgets.QTextBrowser(self.centralwidget)
        self.textArea.setGeometry(QtCore.QRect(270, 101, 601, 401))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI Light")
        font.setPointSize(14)
        self.textArea.setFont(font)
        self.textArea.setObjectName("textArea")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(650, 20, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(720, 20, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.messageArea = QtWidgets.QLineEdit(self.centralwidget)
        self.messageArea.setGeometry(QtCore.QRect(270, 510, 531, 41))
        self.messageArea.setObjectName("messageArea")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(650, 70, 61, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.chat_with = QtWidgets.QTextBrowser(self.centralwidget)
        self.chat_with.setGeometry(QtCore.QRect(720, 60, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.chat_with.setFont(font)
        self.chat_with.setObjectName("chat_with")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Title.setText(_translate("MainWindow", "IMessage"))
        self.sendButton.setText(_translate("MainWindow", "->"))
        __sortingEnabled = self.contacts.isSortingEnabled()
        self.contacts.setSortingEnabled(False)
        item = self.contacts.item(0)
        item.setText(_translate("MainWindow", "Контакты"))
        self.contacts.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("MainWindow", "login:"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Игорь</p></body></html>"))
        self.messageArea.setPlaceholderText(_translate("MainWindow", "Введите текст..."))
        self.label_2.setText(_translate("MainWindow", "Чат с: "))