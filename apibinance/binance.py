import os
from binance.client import Client
from .spot import spot
from .simpleearn import simple_earn
from .stream import stream
from classenum.env import configenv
from flask_socketio import SocketIO
from .historique import historique
class Binance:
    def __init__(self) -> None:
        self.testnet = os.getenv(configenv.TESTNET.value).upper()!="FALSE"
        if self.testnet:
            self.api_secret = os.getenv(configenv.TESTNET_API_SECRET.value)
            self.api_key = os.getenv(configenv.TESTNET_API_KEY.value)
        else:
            self.api_secret = os.getenv(configenv.API_SECRET.value)
            self.api_key = os.getenv(configenv.API_KEY.value)
        self.client = Client(self.api_key , self.api_secret,testnet=self.testnet)
    def get_spot(self) -> spot:
        return spot(self.client)
    def get_earn(self):
        return simple_earn(self.client)
    def get_stream(self,socketio:SocketIO):
        return stream(self.client,socketio)
    def get_historique(self):
        return historique(self.client)