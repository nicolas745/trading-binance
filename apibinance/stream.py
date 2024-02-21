from binance.client import Client ,AsyncClient
from binance.streams import BinanceSocketManager
import time
import asyncio
import threading
from flask_socketio import SocketIO
import os
from classenum.env import configenv
class stream:
    def __init__(self, client:Client,socketio:SocketIO)  -> None:
        self.client = client
        self.socketio = socketio
        threading.Thread(target=self.start).start()
    def start(self):
        loop = asyncio.new_event_loop()  # Créez une nouvelle boucle d'événements
        asyncio.set_event_loop(loop)  # Définissez la nouvelle boucle comme la boucle d'événements pour ce thread
        loop.run_until_complete(self.updateprix())
    def getdata(self):
        return self.data
    async def updateprix(self):
        client = await AsyncClient.create(api_key=self.client.API_KEY, api_secret=self.client.API_SECRET)
        bm = BinanceSocketManager(client)
        ts = bm.trade_socket(f"{os.getenv(configenv.MONEY_ECHANGE.value)}{os.getenv(configenv.MONEY_PRINCIPAL.value)}")  # Vous pouvez également essayer bm.futures_user_socket()
        async with ts as tscm:
            while True:
                time.sleep(5)
                res = await tscm.recv()
                self.socketio.emit("prix",res['p'])