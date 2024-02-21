from binance.client import Client
from .apispot.balances import balances

class spot:
    def __init__(self, client: Client) -> None:
        self.client = client
    
    def get_account_data(self):
        return self.client.get_account()
    
    def get_balances(self) -> balances:
        return balances(self.get_account_data())
    
    def buy_market(self, symbol, quantity):
        order = self.client.create_order(symbol=symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=quantity)
        return order
    
    def sell_market(self, symbol, quantity):
        order = self.client.create_order(symbol=symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET, quantity=quantity)
        return order
    
    def buy_limit(self, symbol, quantity, price):
        time_in_force = Client.TIME_IN_FORCE_GTC
        order = self.client.create_order(symbol=symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_LIMIT, quantity=quantity, price=price, timeInForce=time_in_force)
        return order
    
    def sell_limit(self, symbol, quantity, price):
        time_in_force = Client.TIME_IN_FORCE_GTC
        order = self.client.create_order(symbol=symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_LIMIT, quantity=quantity, price=price, timeInForce=time_in_force)
        return order

