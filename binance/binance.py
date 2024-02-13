import requests
import hmac
import hashlib
import time
import os
from spot import spot
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
        timestamp = int(time.time() * 1000)
        query_string = 'timestamp=' + str(timestamp)
        signature = hmac.new(bytes(self.api_secret , 'latin-1'), msg = bytes(query_string , 'latin-1'), digestmod = hashlib.sha256).hexdigest()

        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        url = self.base_url+"api/v3/account?" + query_string + "&signature=" + signature
        response = requests.get(url, headers=headers)
        return spot(response.json())