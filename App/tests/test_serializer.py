
import json
from chat.serializer import Serializer
from chat.messages import Authenticate


def test_serialize_authenticate():
    msg = Authenticate('Igor', '123')

    expected_time = 123
    expected_msg = {
        "action": "authenticate",
        "time": expected_time,
        "user": {
            "account_name": msg.account_name,
            "password": msg.password
        }
    }
    expected_data = json.dumps(expected_msg).encode('utf-8')

    sut = Serializer(json.dumps, 'utf-8', get_time=lambda: expected_time)
    assert sut.serialize(msg) == expected_data
