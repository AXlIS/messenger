import sqlite3
from dataclasses import dataclass


@dataclass
class ClientInfo:
    login: str
    password: str


class ClientStorage:
    def __init__(self, conn) -> None:
        self._conn = conn

    def add(self, login, info):
        pass

    def find(self, client_id):
        pass

    def get(self, client_id):
        cursor = self._conn.cursor()
        cursor.execute("SELECT login, password FROM ...")

        row = cursor.fetchone()
        return ClientInfo(login=row[0], password=row[1])


@dataclass
class ClientHistory:
    connect_time: time
    address: str
