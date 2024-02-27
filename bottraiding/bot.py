from sql.trading import TradingDatabase
from classenum.sql import enumsql
from classenum.env import configenv
from datetime import datetime
import os
from binance.client import AsyncClient
from apibinance.spot import spot
from apibinance.simpleearn import simple_earn
from datetime import datetime
class bot:
    def __init__(self, data, db:TradingDatabase,client:AsyncClient) -> None:
        self.db = db
        self.client = client
        self.data = {}
        self.data['time'] = data["T"]/1000
        self.data["prix"] = data["p"]
        self.moneyprincipal= os.getenv(configenv.MONEY_PRINCIPAL.value)
        self.moneyechange= os.getenv(configenv.MONEY_ECHANGE.value)
        self.date = enumsql.DATE.value

    def start(self):
        #myspot = spot(self.client)
        #comptespot = {
        #    configenv.MONEY_ECHANGE.value:myspot.get_balances().getactifechange(),
        #    configenv.MONEY_PRINCIPAL.value:myspot.get_balances().getactifprincal()
        #}
        #myearn = simple_earn(self.client)
        #comptflexible = {
        #    configenv.MONEY_ECHANGE.value:myearn.getflexible().getvaleurmoneyechange(),
        #    configenv.MONEY_PRINCIPAL.value:myearn.getflexible().getvaleurmoneyprincipal()
        #}
        orders = self.db.get_all_orders()
        if orders.__len__():
           for order in orders:
                pricipal= order[self.moneyprincipal]
                actif=order[self.moneyechange]
                lastdate=datetime.strptime(order[self.date], "%Y-%m-%dT%H:%M").timestamp()
                nowdate = datetime.now().timestamp()
                defdate=nowdate-lastdate
                prix = pricipal/actif
                newprix = prix * pow(1 + 0.001, 2) * pow(1 + 0.06 / (365 * 24 * 60 * 60), defdate)
                pourcentage=(pricipal+((float(self.data['prix'])-newprix)*actif))/pricipal-1
                if 0.012<pourcentage:
                    spot(self.client).sell_market(order['id'])
        user=self.db.get_portfolio_data()
        time=(datetime.now().timestamp()-datetime.strptime(user[self.date], "%Y-%m-%dT%H:%M").timestamp())
        if(60*60*12<time):
            buy=10
            nborder =user[enumsql.NBEXORDER.value]
            nborderdouble=user[enumsql.NBEXORDERDOUBLE.value]
            newbuy=buy*pow(1.01,user[enumsql.NBEXORDERDOUBLE.value])
            quantite = newbuy/self.data["prix"]