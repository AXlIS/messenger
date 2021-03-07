import json
from time import time
from chat.messages import Authenticate


class Serializer:
    def __init__(self, dumps=json.dumps, encoding='utf-8', get_time=time):
        self._dumps = dumps
        self._encoding = encoding
        self._get_time = get_time

    def serialize(self, msg):
        if isinstance(msg, Authenticate):
            result_dict = {
                "action": "authenticate",
                "time": self._get_time(),
                "user": {
                    "account_name": msg.account_name,
                    "password": msg.password
                }
            }
            result_str = self._dumps(result_dict)
            return result_str.encode(self._encoding)
