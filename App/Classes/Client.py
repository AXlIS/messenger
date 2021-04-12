from dataclasses import dataclass
from socket import socket


@dataclass
class ClientItem:
    id: int
    socket: socket
