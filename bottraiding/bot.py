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
        #myearn = simple_earn(self.client)
        #comptflexible = {
        #    configenv.MONEY_ECHANGE.value:myearn.getflexible().getmyposition(),
        #    configenv.MONEY_PRINCIPAL.value:myearn.getflexible()
        #}
        ##myspot.get_balances()
        #orders = self.db.get_all_orders()
        #compte = {}
        #compteearn={}
        #for wallet in self.client.get_account()['balances']:
        #    if(wallet['asset']==os.getenv(configenv.MONEY_ECHANGE.value).upper()):
        #        compte[os.getenv(configenv.MONEY_ECHANGE.value)] = wallet['free']
        #    if(wallet['asset']==os.getenv(configenv.MONEY_PRINCIPAL.value).upper()):
        #        compte[os.getenv(configenv.MONEY_PRINCIPAL.value)] = wallet['free']
        ##for earn in self.client.get_simple_earn_account():
        ##    if(os.getenv(configenv.MONEY_ECHANGE.value).upper() in earn):
        ##        compteearn[os.getenv(configenv.MONEY_ECHANGE.value)] = self.client.get_simple_earn_account()[earn]
        ##    if(os.getenv(configenv.MONEY_PRINCIPAL.value).upper() in earn):
        ##        compteearn[os.getenv(configenv.MONEY_PRINCIPAL.value)] = self.client.get_simple_earn_account()[earn]
        #for order in orders:
        #    print(order[enumsql.DATE.value])
        #    date_time_object = datetime.strptime(order[enumsql.DATE.value], "%Y-%m-%dT%H:%M")
        #    timestamp = date_time_object.timestamp()
        #    timedif = self.data['time'] - timestamp
        #    prix = order[enumsql.QUANTITEACTIF.value] / order[enumsql.QUANTITEPRINCIPAL.value]
        #    calcprix = prix * pow(1 + 0.05 / (365 * 24 * 60 * 60), timedif)
        #    
        #    #if(float(self.data["prix"]) / calcprix):
        #    #    res=False
        #    #    if(float(order[enumsql.QUANTITEACTIF.value])>float(compte[configenv.MONEY_ECHANGE.value])):
        #    #        if(float(compteearn[os.getenv(configenv.MONEY_ECHANGE.value)])>=float(order[enumsql.QUANTITEACTIF.value])):
        #    #            res=True
        #    #    else:
        #    #        res=True
        #    #    if res:
        #    #        symbol="{}{}".format(os.getenv(configenv.MONEY_ECHANGE.value),os.getenv(configenv.MONEY_PRINCIPAL.value))
        #    #        self.client.order_market_buy(symbol=symbol,quantity=order[enumsql.QUANTITEACTIF.value])
        #    #        self.db.delete_order(order['id'])