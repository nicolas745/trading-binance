
from bottoapi.binance.spot import spot
from flask_socketio import SocketIO
class orders:
    def __init__(self,client) -> None:
        self.client = client
    def sell(self,Socketio:SocketIO,order):
        spot(self.client).sell_market(order['id'])
        Socketio.emit("del",order['id'])
    def buy(self):
        pass