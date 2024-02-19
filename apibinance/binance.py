import os
from binance.client import Client

from .spot import spot
from .simpleearn import simple_earn
from classenum.env import configenv
from dotenv import load_dotenv
load_dotenv()
class Binance:
    def __init__(self) -> None:
        self.testnet = bool(os.getenv(configenv.TESTNET.value))
        if self.testnet:
            self.api_secret = os.getenv(configenv.TESTNET_API_SECRET.value)
            self.api_key = os.getenv(configenv.TESTNET_API_KEY.value)
        else:
            self.api_secret = os.getenv(configenv.API_SECRET.value)
            self.api_key = os.getenv(configenv.API_KEY.value)
        self.client = Client(self.api_key , self.api_secret,testnet=self.testnet)
        Client.transfer_history()
    def get_spot(self) -> spot:
        return spot(self.client)
    def get_earn(self):
        return simple_earn(self.client)