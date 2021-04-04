class Port:
    def __init__(self, default):
        self.default = default
        self.name = None

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f'TypeError')

        if not 0 < value <= 65365:
            print(000000)
            raise ValueError(f'ValueError')

        setattr(instance, self.name, value)


class Server:
    port = Port(7777)


server = Server()
server.port = 3.6
server.port = 400000
print(server.port)
