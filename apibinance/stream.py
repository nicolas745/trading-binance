from binance.client import Client
from binance.streams import BinanceSocketManager
import time
import threading
import os
from classenum.env import configenv
class stream:
    def __init__(self, client:Client)  -> None:
        self.client = client
        threading.Thread(target=self.prix).start()
    async def start(self):
        client = Client("api_key", "api_secret")
        bm = BinanceSocketManager(client)
        ts = bm.trade_socket("{}{}".format(os.getenv(configenv.MONEY_PTINCIPAL.value),os.getenv(configenv.MONEY_ECHANGE)))
        async with ts as tscm:
            while(True):
                time.sleep(1)
                res = await tscm.recv()
                print(res)
    def update(self,data):
        print(data)

