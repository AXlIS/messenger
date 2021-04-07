import select
from socket import AF_INET, SOCK_STREAM, socket
import click
from datetime import datetime
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Client, ClientHistoryStorage


class Server:

    def __init__(self):
        engine = create_engine("sqlite:///database.db", echo=True)
        self.Session = sessionmaker(bind=engine)

        self.clients = []
        self.main(7777, 'localhost')

    def disconnect(self, sock):
        print(f"Клиент {sock.fileno()} {sock.getpeername()} отключен")
        self.clients.remove(sock)

    def read(self, read_clients):
        responses = {}

        for sock in read_clients:
            try:
                data = sock.recv(1024)
                user = json.loads(data.decode('utf-8'))
                if user['action'] == 'authenticate':
                    with self.Session() as session:
                        client = session.query(Client).filter(Client.login == user["login"]).first()
                        if client and client.password == user["password"]:
                            history_storage = ClientHistoryStorage(session)
                            history_storage.add_line(ip=sock.getpeername()[0], client_id=client.id, status='login')
                            sock.send(json.dumps(
                                {"response": "202",
                                 'message': 'Вы вошли в чат!'}
                            ).encode('utf-8'))
                        else:
                            sock.send(json.dumps(
                                {"response": "400",
                                 'message': "Что-то пошло не так.."}
                            ).encode('utf-8'))
                            self.disconnect(sock)
                elif user['action'] == 'send_message':
                    responses[sock] = data
            except:
                self.disconnect(sock)
                pass

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

    # @click.command()
    # @click.option("--port", default=7777)
    # @click.option("--addr", default='localhost')
    def main(self, port, addr):

        with socket(AF_INET, SOCK_STREAM) as s:
            try:
                s.bind((addr, port))
                s.listen(5)
                s.settimeout(0.2)

                while True:
                    try:
                        client, addr = s.accept()
                    except OSError:
                        pass
                    else:
                        print(f"Получен запрос на соединение от {client}")
                        self.clients.append(client)
                    finally:
                        wait = 0
                        r = []
                        w = []
                        try:
                            r, w, e = select.select(self.clients, self.clients, [], wait)
                        except:
                            pass

                        requests = self.read(r)
                        self.write(requests, w)
            finally:
                for sock in self.clients:
                    sock.close()


if __name__ == '__main__':
    server = Server()
