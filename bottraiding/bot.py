from sql.trading import TradingDatabase
from classenum.sql import enumsql
from classenum.env import configenv
from datetime import datetime
import os
from binance.client import AsyncClient
from apibinance.spot import spot
from apibinance.simpleearn import simple_earn
class bot:
    def __init__(self, data, db:TradingDatabase,client:AsyncClient) -> None:
        self.db = db
        self.client = client
        self.data = {}
        self.data['time'] = data["T"]/1000
        self.data["prix"] = data["p"]

    def start(self):
        myspot = spot(self.client)
        comptespot = {
            configenv.MONEY_ECHANGE.value:myspot.get_balances().getactifechange(),
            configenv.MONEY_PRINCIPAL.value:myspot.get_balances().getactifprincal()
        }
        myearn = simple_earn(self.client)
        #comptflexible = {
        #    configenv.MONEY_ECHANGE.value:myearn.getflexible().getvaleurmoneyechange(),
        #    configenv.MONEY_PRINCIPAL.value:myearn.getflexible().getvaleurmoneyprincipal()
        #}
        user=self.db.get_portfolio_data()
        orders = self.db.get_all_orders()
        for order in orders:
            print(user)