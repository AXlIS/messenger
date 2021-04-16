from dataclasses import dataclass
from socket import socket


@dataclass
class ClientItem:
    id: int
    login: str
    socket: socket