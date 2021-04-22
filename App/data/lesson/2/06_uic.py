import sys
from pathlib import Path

from icecream import ic
from PyQt5 import QtWidgets, uic

from pyqt5_helper import setup_plugin_path

if __name__ == "__main__":
    setup_plugin_path()

    app = QtWidgets.QApplication(sys.argv)

    ui_file_path = Path(__file__).parent.absolute() / "06_form.ui"
    window = uic.loadUi(ui_file_path)

    window.btnQuit.clicked.connect(app.quit)
    window.textEdit.textChanged.connect(lambda: ic(window.textEdit.toPlainText()))

    window.show()
    sys.exit(app.exec_())
