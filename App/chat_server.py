import select
from socket import AF_INET, SOCK_STREAM, socket
import click
import json


# def disconnect(sock, all_clients):
# print(f"Клиент {sock.fileno()} {sock.getpeername()} отключен")
# all_clients.remove(sock)


def read(read_clients, all_clients):
    responses = {}

    for sock in read_clients:
        try:
            data = sock.recv(1024)
            action = json.loads(data.decode('utf-8'))['action']
            if action == 'authenticate':
                sock.send(json.dumps({'action': 'sending_message', 'message': 'Вы вошли в чат!'}).encode('utf-8'))
            elif action == 'send_message':
                responses[sock] = data
        except:
            # disconnect(sock, all_clients)
            pass

    return responses


def write(requests, write_clients, all_clients):
    for sock in write_clients:
        for recv_sock, data in requests.items():
            if sock is recv_sock:
                continue
            try:
                resp = data
                sock.send(resp)
            except:
                # disconnect(sock, all_clients)
                pass


@click.command()
@click.option("--port", default=7777)
@click.option("--addr", default='localhost')
def main(port, addr):
    clients = []

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
                    clients.append(client)
                finally:
                    wait = 0
                    r = []
                    w = []
                    try:
                        r, w, e = select.select(clients, clients, [], wait)
                    except:
                        pass

                    requests = read(r, clients)
                    write(requests, w, clients)
        finally:
            for sock in clients:
                sock.close()


if __name__ == '__main__':
    main()
