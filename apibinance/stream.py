from binance.client import Client ,AsyncClient
from binance.streams import BinanceSocketManager
import time
import asyncio
import threading
import os
from classenum.env import configenv
class stream:
    def __init__(self, client:Client)  -> None:
        self.client = client
        threading.Thread(target=self.start).start()
    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.updateprix())
    def getdata(self,data):
        print(data)
    async def updateprix(self):
        client = await AsyncClient.create(api_key=self.client.API_KEY, api_secret=self.client.API_SECRET)
        bm = BinanceSocketManager(client)
        ts = bm.futures_socket()  # Vous pouvez également essayer bm.futures_user_socket()
        async with ts as tscm:
            while True:
                res = await tscm.recv()
                print(res)