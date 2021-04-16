import select
from socket import AF_INET, SOCK_STREAM, socket
import json
from hashlib import pbkdf2_hmac

from icecream import ic
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Client, ClientHistoryStorage
from DataClasses.Client import ClientItem


class Server:

    def __init__(self):
        engine = create_engine("sqlite:///database.db", echo=True)
        self.Session = sessionmaker(bind=engine)

        self.clients = []
        self.main(7777, 'localhost')

    def check_password(self, password, client):
        from_user = pbkdf2_hmac(hash_name='sha256', password=password.encode('utf-8'),
                                salt=client.login.encode('utf-8'), iterations=100)
        return from_user == client.password

    def disconnect(self, sock):
        ic(self.clients)
        ic(f"Клиент {sock.fileno()} {sock.getpeername()} отключен")
        self.clients = list(filter(lambda x: x.socket != sock, self.clients))

    def read(self, read_clients):
        responses = {}

        for sock in read_clients:
            try:
                data = sock.recv(1024)
                user = json.loads(data.decode('utf-8'))
                ic(user)
                if user['action'] == 'authenticate':
                    with self.Session() as session:
                        client = session.query(Client).filter(Client.login == user["login"]).first()
                        if client and self.check_password(user["password"], client):
                            history_storage = ClientHistoryStorage(session)
                            history_storage.add_line(ip=sock.getpeername()[0], client_id=client.id, status='login')
                            for item in self.clients:
                                if item.socket == sock:
                                    item.id, item.login = client.id, client.login
                            sock.send(json.dumps(
                                {"response": 202,
                                 "action": "authenticate",
                                 "user_id": client.id,
                                 'message': 'Вы вошли в чат!'}
                            ).encode('utf-8'))
                        else:
                            sock.send(json.dumps(
                                {"response": 400,
                                 "action": "authenticate",
                                 'message': "Что-то пошло не так.."}
                            ).encode('utf-8'))
                            self.disconnect(sock)
                elif user['action'] == 'sending':
                    ic(data)
                    responses[user["to"]] = data
                    ic(responses)
            except:
                self.disconnect(sock)
                pass

        return responses

    def write(self, requests, write_clients):
        # for sock in write_clients:
        #     for recv_sock, data in requests.items():
        #         if sock is recv_sock:
        #             continue
        #         try:
        #             resp = data
        #             sock.send(resp)
        #         except:
        #             self.disconnect(sock)
        #             pass
        for user in self.clients:
            for recv_name, data in requests.items():
                if recv_name == user.login:
                    try:
                        user.socket.send(data)
                    except:
                        self.disconnect(user.socket)

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
                        self.clients.append(ClientItem(0, '', client))
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
                for sock in self.clients:
                    sock.close()


if __name__ == '__main__':
    server = Server()
