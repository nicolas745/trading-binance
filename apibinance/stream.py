from binance.client import Client ,AsyncClient
from binance.streams import BinanceSocketManager
import time
import asyncio
import threading
from sql.trading import TradingDatabase
from flask_socketio import SocketIO
import os
from bottraiding.bot import bot
from classenum.env import configenv
from classenum.sql import enumsql
class stream:
    def __init__(self, client:Client,socketio:SocketIO)  -> None:
        self.client = client
        self.socketio = socketio
        self.prix = 0
        self.buytime = 0
        self.sellprix = 0
    def start(self):
        threading.Thread(target=self.load).start()
    def load(self):
        loop = asyncio.new_event_loop()  # Créez une nouvelle boucle d'événements
        asyncio.set_event_loop(loop)  # Définissez la nouvelle boucle comme la boucle d'événements pour ce thread
        loop.run_until_complete(self.updateprix())
    async def updateprix(self):
        client = await AsyncClient.create(api_key=self.client.API_KEY, api_secret=self.client.API_SECRET)
        bm = BinanceSocketManager(client)
        ts = bm.trade_socket(f"{os.getenv(configenv.MONEY_ECHANGE.value)}{os.getenv(configenv.MONEY_PRINCIPAL.value)}")  # Vous pouvez également essayer bm.futures_user_socket()
        db = TradingDatabase()
        async with ts as tscm:
            mybot = bot(db,self.client)
            while True:
                res = await tscm.recv()
                self.socketio.emit("prix",res['p'])
                self.prix = res['p']
                mybot.start(self.prix,self.socketio)
                self.sellprix=mybot.getsellprix()
                self.buytime=mybot.getbuytime()
                self.socketio.emit("buytime",self.buytime)
                self.socketio.emit("sellprix",self.sellprix)
                time.sleep(1)
    def getprix(self):
        return self.prix
    def getsellprix(self):
        return self.sellprix
    def getbuytime(self):
        return self.buytime
