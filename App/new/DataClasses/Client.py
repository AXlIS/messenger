from dataclasses import dataclass
from socket import socket


@dataclass
class ClientItem:
    """DTO for a client"""
    id: int  #: Client id
    login: str  #: Client login
    socket: socket  #: Client socket
