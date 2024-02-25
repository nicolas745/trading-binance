from binance.client import Client, AsyncClient
from .apispot.balances import balances
from .simple_earn.flexible import flexible
from classenum.env import configenv
from classenum.sql import enumsql
from sql.trading import TradingDatabase
import os
class spot:
    def __init__(self, client: Client|AsyncClient) -> None:
        self.client = client
        self.symbol = "{}{}".format(os.getenv(configenv.MONEY_ECHANGE.value),os.getenv(configenv.MONEY_PRINCIPAL.value)).upper()
    def get_account_data(self):
        return self.client.get_account()
    def get_balances(self) -> balances:
        return balances(self.client.get_account())
    
    def buy_market(self, quantity,prix):
        if(float(self.getinfo())<float(quantity)):
            db = TradingDatabase()
            portfolio=db.get_portfolio_data()
            principal=portfolio[enumsql.QUANTITEPRINCIPAL.value]
            if(quantity*prix<principal):
                order=self.client.create_order(symbol=self.symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=quantity)
                if(order['status']=="FILLED"):
                    db.add_order(order["executedQty"],order["cummulativeQuoteQty"])
            return False
    
    def sell_market(self, id):
        db = TradingDatabase()
        order=db.get_order(id)
        quantA = order[enumsql.QUANTITEACTIF.value]
        order = self.client.create_order(symbol=self.symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET, quantity=quantA)
    
    def buy_limit(self, quantity, price):
        time_in_force = Client.TIME_IN_FORCE_GTC
        order = self.client.create_order(symbol=self.symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_LIMIT, quantity=quantity, price=price, timeInForce=time_in_force)
        return order
    
    def sell_limit(self, quantity, price):
        time_in_force = Client.TIME_IN_FORCE_GTC
        order = self.client.create_order(symbol=self.symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_LIMIT, quantity=quantity, price=price, timeInForce=time_in_force)
        return order
    def getinfo(self):
        datas=self.client.get_symbol_info(self.symbol)['filters']
        for data in datas:
            if(data['filterType']=="LOT_SIZE"):
                return data['minQty']