from binance.client import Client, AsyncClient
from .apispot.balances import balances
from .simple_earn.flexible import flexible
from classenum.env import configenv
import os
class spot:
    def __init__(self, client: Client|AsyncClient) -> None:
        self.client = client
        self.symbol = "{}{}".format(configenv.MONEY_ECHANGE.value,configenv.MONEY_PRINCIPAL.value)
    def get_account_data(self):
        return self.client.get_account()
    def get_balances(self) -> balances:
        return balances(self.client.get_account())
    
    def buy_market(self, quantity):
        order = self.client.create_order(symbol=self.symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=quantity)
        return order
    
    def sell_market(self, quantity):
        order = self.client.create_order(symbol=self.symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET, quantity=quantity)
        return order
    
    def buy_limit(self, quantity, price):
        time_in_force = Client.TIME_IN_FORCE_GTC
        order = self.client.create_order(symbol=self.symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_LIMIT, quantity=quantity, price=price, timeInForce=time_in_force)
        return order
    
    def sell_limit(self, quantity, price):
        time_in_force = Client.TIME_IN_FORCE_GTC
        order = self.client.create_order(symbol=self.symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_LIMIT, quantity=quantity, price=price, timeInForce=time_in_force)
        return order

