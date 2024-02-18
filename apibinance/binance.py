import requests
import hmac
import hashlib
import time
import os
from binance.client import Client

from .spot import spot
from .simpleearn import simple_earn
from dotenv import load_dotenv
load_dotenv()
class Binance:
    def __init__(self) -> None:
        self.testnet = bool(os.getenv("testnet"))
        if self.testnet:
            self.api_secret = os.getenv("testnet_api_secret")
            self.api_key = os.getenv("testnet_api_key")
        else:
            self.api_secret = os.getenv("api_secret")
            self.api_key = os.getenv("api_key")
        self.client = Client(self.api_key , self.api_secret,testnet=self.testnet)
    def get_spot(self) -> spot:
        return spot(self.client.get_account())
    def get_earn(self):
        return simple_earn(self.client)