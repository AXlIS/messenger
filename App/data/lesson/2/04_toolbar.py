# ---------------- Графический интерфейс пользователя. PyQt5 ------------------
#                   Демонстрация создания событий (Action)

"""
ZetCode PyQt5 tutorial

This program creates a toolbar.
The toolbar has one action, which terminates the application, if triggered.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, qApp

from pyqt5_helper import setup_plugin_path


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exitAction = QAction(QIcon("exit.svg"), "Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar("Exit")
        self.toolbar.addAction(exitAction)

        self.setGeometry(500, 300, 900, 600)
        self.setWindowTitle("Toolbar")
        self.show()


if __name__ == "__main__":
    setup_plugin_path()

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
