import os
from .spot import spot
from .simpleearn import simple_earn
class default:
    def __init__(self) -> None:
        pass
    def get_spot(self) -> spot:
        return spot()
    def get_earn(self) -> simple_earn:
        return simple_earn()
    def get_stream(self,socketio:SocketIO):
        return stream(self.client,socketio)
    def get_historique(self):
        return historique(self.client)