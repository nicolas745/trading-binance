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
    def __init__(self, testnet: bool = False) -> None:
        if testnet:
            self.api_secret = os.getenv("testnet_api_secret")
            self.api_key = os.getenv("testnet_api_key")
            self.base_url = "https://testnet.binance.vision/"
        else:
            self.base_url = "https://api.binance.com/"
            self.api_secret = os.getenv("api_secret")
            self.api_key = os.getenv("api_key")
    def get_spot(self) -> spot:
        binance_api_key = self.api_key
        binance_secret_key = self.api_secret
        client = Client(binance_api_key, binance_secret_key,testnet=False)
        response = client.get_account()
        print(response)
        return spot(response)
    def get_earn(self):
        return simple_earn(self.base_url,self.api_secret,self.api_key)