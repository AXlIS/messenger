import sys
from pathlib import Path

from icecream import ic
from PyQt5 import QtWidgets, uic

from pyqt5_helper import setup_plugin_path


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file_path = Path(__file__).parent.absolute() / "06_form.ui"
        uic.loadUi(ui_file_path, self)

        self.btnQuit.clicked.connect(QtWidgets.qApp.quit)
        self.textEdit.textChanged.connect(self.on_text_changed)

    def on_text_changed(self):
        ic(self.textEdit.toPlainText())


if __name__ == "__main__":
    setup_plugin_path()

    app = QtWidgets.QApplication(sys.argv)

    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
