from binance.client import Client
from .apispot.balances import balances
class spot:
    def __init__(self,client:Client) -> None:
        self.client = client
    def get_data(self):
        return self.get_data()
    def getbalances(self) -> balances:
        return balances(self.get_data())
    def market(self, symbol, side, quantity):
        order = self.client.create_order(symbol=symbol, side=side, type=Client.ORDER_TYPE_MARKET, quantity=quantity)
        return order
    def limit(self, symbol, side, quantity, price):
        time_in_force = Client.TIME_IN_FORCE_GTC
        order = self.client.create_order(symbol=symbol, side=side, type=Client.ORDER_TYPE_LIMIT, quantity=quantity, price=price, timeInForce=time_in_force)
        return order
