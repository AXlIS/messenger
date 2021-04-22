class Port:
    def __init__(self, default=7777):
        self.default = default
        self.name = None

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f'TypeError')

        if not 0 < value <= 65365:
            raise ValueError(f'ValueError')

        setattr(instance, self.name, value)

    def __set_name__(self, cls, name):
        self.name = f'__{name}'


class Server:
    port = Port()


server = Server()

server.port = 60000
print(server.port)
# server.port = 1000
# server.port = 3.6
# server.port = 4000
# print(server.port)
