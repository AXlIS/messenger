from chat.client import Client
from unittest.mock import MagicMock
from chat.messages import Authenticate


def test_authenticate():
    mock_sock = MagicMock()
    mock_serializer = MagicMock()
    sub = Client(mock_sock, "username", mock_serializer)

    mock_serializer.serialize.return_value = b'123TEST'

    sub.authenticate('password')

    mock_serializer.serialize.assert_called_once_with(
        Authenticate("username", "password")
    )