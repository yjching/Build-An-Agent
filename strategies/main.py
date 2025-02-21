from clients.main import BaseClient

class ReflectionStrategy():
    def __init__(self, clients: dict[BaseClient, BaseClient]):
        self._clients = clients
    @property
    def clients(self):
        return self._clients

    @clients.setter
    def clients(self, value):
        self._clients = value
