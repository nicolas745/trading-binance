from binance.client import Client
from binance.streams import BinanceSocketManager
import time
import threading
class stream:
    def __init__(self, client:Client)  -> None:
        self.client = client
        threading.Thread(target=self.prix).start()
    def start(self):
        client = Client("api_key", "api_secret")
        bm = BinanceSocketManager(client)
        conn_key = bm.start_symbol_ticker_socket('BTCUSDT', self.update)
        while(True):
            time.sleep(60)
            bm.start()
    def update(self,data):
        print(data)

