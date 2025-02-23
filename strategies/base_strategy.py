class BaseStrategy():
    def __init__(self, base_client):
        self.base_client = base_client
    @property
    def clients(self):
        return self._clients
    @clients.setter
    def clients(self, value):
        self._clients = value
