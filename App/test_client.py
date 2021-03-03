import unittest
from client import client
from time import time


class TestClient(unittest.TestCase):

    def test_client(self):
        self.assertEqual(client(7777, 'localhost'), {'action': 'probe', 'time': f'<{int(time()) // 10000}>'})


if __name__ == "__main__":
    unittest.main()
