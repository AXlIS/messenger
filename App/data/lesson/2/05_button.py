import sys

from PyQt5 import QtWidgets

from pyqt5_helper import setup_plugin_path


def on_clicked():
    print("Кнопка нажата. Функция on_clicked")


class MyClass:
    def on_clicked(self):
        print("Кнопка нажата. Метод MyClass.on_clicked()")


class MyCallable:
    def __init__(self, x=0):
        self.x = x

    def __call__(self):
        print("Кнопка нажата. Метод MyClass.__call__()")
        print("x = ", self.x)


if __name__ == "__main__":
    setup_plugin_path()

    obj = MyClass()
    my_callable = MyCallable(10)
    app = QtWidgets.QApplication(sys.argv)
    button = QtWidgets.QPushButton("Нажми меня")

    # В качестве обработчика назначается функция
    button.clicked.connect(on_clicked)

    # В качестве обработчика назначается метод объекта
    button.clicked.connect(obj.on_clicked)

    # В качестве обработчика назначается экземпляр класса
    button.clicked.connect(my_callable)

    # В качестве обработчика назначается lambda-функция
    button.clicked.connect(lambda: print("Кнопка нажата. Lambda"))

    button.show()
    sys.exit(app.exec_())
