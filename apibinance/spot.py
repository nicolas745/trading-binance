from binance.client import Client, AsyncClient
from .apispot.balances import balances
from .simple_earn.flexible import flexible
from classenum.env import configenv
from classenum.sql import enumsql
from sql.trading import TradingDatabase
from datetime import datetime
import os
class spot:
    def __init__(self, client: Client|AsyncClient) -> None:
        self.client = client
        self.symbol = "{}{}".format(os.getenv(configenv.MONEY_ECHANGE.value),os.getenv(configenv.MONEY_PRINCIPAL.value)).upper()
    def get_balances(self) -> balances:
        return balances(self.client.get_account())
    
    def buy_market(self, quantity,prix):
        quantity=round(float(quantity)/float(self.getinfo()))*float(self.getinfo())
        if(float(self.getinfo())<float(quantity)):
            db = TradingDatabase()
            portfolio=db.get_portfolio_data()
            principal=float(portfolio[os.getenv(configenv.MONEY_PRINCIPAL.value)])
            if(float(quantity)*float(prix)<principal):
                order=self.client.create_order(symbol=self.symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=quantity)
                if(order['status']=="FILLED"):
                    db.add_order(order["cummulativeQuoteQty"],quantity, datetime.now().strftime("%Y-%m-%dT%H:%M"))
                    db.buy(order["cummulativeQuoteQty"],quantity)
                    return True
            return False
    def sell_market(self, id):
        db = TradingDatabase()
        order=db.get_order(id)
        if order.__len__():
            quantA = order[0][os.getenv(configenv.MONEY_ECHANGE.value)]
            order = self.client.create_order(symbol=self.symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET, quantity=quantA)
            if(order['status']=="FILLED"):
                db.delete_order(id)
                db.sell(order["cummulativeQuoteQty"],quantA)
                return True
        return False
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