import select
from socket import AF_INET, SOCK_STREAM, socket
import click
from datetime import datetime
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Client, ClientHistoryStorage
from icecream import ic
from Classes.Client import ClientItem


class Server:

    def __init__(self):
        engine = create_engine("sqlite:///database.db", echo=True)
        self.Session = sessionmaker(bind=engine)

        self.clients = []
        self.main(7777, 'localhost')

    def disconnect(self, sock):
        ic(f"Клиент {sock.fileno()} {sock.getpeername()} отключен")
        disconnect_client = next(client for client in self.clients if client.socket == sock)
        if disconnect_client.id != 0:
            with self.Session() as session:
                ic(sock)
                history_storage = ClientHistoryStorage(session)
                history_storage.add_line(ip=sock.getpeername()[0], client_id=disconnect_client.id, status='quit')
        sock.close()
        self.clients = list(filter(lambda x: x.socket != sock, self.clients))
        ic(self.clients)

    def read(self, read_clients):
        responses = {}

        for sock in read_clients:
            # try:
            data = sock.recv(100000)
            ic(data)
            user = json.loads(data.decode('utf-8'))
            if user['action'] == 'authenticate':
                with self.Session() as session:
                    client = session.query(Client).filter(Client.login == user["login"]).first()
                    if client and client.password == user["password"]:
                        #     # history_storage = ClientHistoryStorage(session)
                        #     # history_storage.add_line(ip=sock.getpeername()[0], client_id=client.id, status='login')
                        #     for item in self.clients:
                        #         if item.socket == sock:
                        #             item.id = client.id
                        sock.send(json.dumps(
                            {"response": 202,
                             "action": "authenticate",
                             'message': 'Вы вошли в чат!'}
                        ).encode('utf-8'))
                    else:
                        sock.send(json.dumps(
                            {"response": 400,
                             "action": "authenticate",
                             'message': "Что-то пошло не так.."}
                        ).encode('utf-8'))
                        self.disconnect(sock)
            # elif user['action'] == 'send_message':
            #     responses[sock] = data
        # self.disconnect(sock)
        # pass
        return responses

    def write(self, requests, write_clients):

        for sock in write_clients:
            for recv_sock, data in requests.items():
                if sock is recv_sock:
                    continue
                try:
                    resp = data
                    sock.send(resp)
                except:
                    self.disconnect(sock)
                    pass

    def main(self, port, addr):

        with socket(AF_INET, SOCK_STREAM) as s:
            try:
                s.bind((addr, port))
                s.listen(5)
                s.settimeout(0.2)

                while True:
                    try:
                        client, addr = s.accept()
                        print('')
                        ic(client)
                        print('')
                    except OSError:
                        pass
                    else:
                        print(f"Получен запрос на соединение от {client}")
                        self.clients.append(ClientItem(0, client))
                    finally:
                        wait = 0
                        r = []
                        w = []
                        select_clients = [client.socket for client in self.clients]
                        try:
                            r, w, e = select.select(select_clients, select_clients, [], wait)
                        except:
                            pass

                        requests = self.read(r)
                        self.write(requests, w)
            finally:
                for sock in [client.socket for client in self.clients]:
                    sock.close()


if __name__ == '__main__':
    server = Server()
