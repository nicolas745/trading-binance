from sql.trading import TradingDatabase
from classenum.sql import enumsql
from classenum.env import configenv
from datetime import datetime
import os
import numpy as np
from flask_socketio import SocketIO
from api.binance.client import AsyncClient
from bottoapi.binance.spot import spot
from bottoapi.binance.simpleearn import simple_earn
from datetime import datetime, timedelta
from .order import orders as buysell
res = True
class bot:
    def __init__(self, db:TradingDatabase,client:AsyncClient) -> None:
        self.db = db
        self.client = client
        self.moneyprincipal= os.getenv(configenv.MONEY_PRINCIPAL.value)
        self.moneyechange= os.getenv(configenv.MONEY_ECHANGE.value)
        self.date = enumsql.DATE.value
        self.res = True
        self.sellprix = 0
        self.time = 0
    def start(self, actifprix,Socketio:SocketIO):
        executorder=0
        actifprix = float(actifprix)
        orders = self.db.get_all_orders()
        if self.sellprix < actifprix/1.01:
            self.sellprix = actifprix/1.01
        elif actifprix <self.sellprix:
            self.sellprix = actifprix
        if orders.__len__():
            for order in orders:
                pricipal= order[self.moneyprincipal]
                actif=order[self.moneyechange]
                lastdate=datetime.strptime(order[self.date], "%Y-%m-%dT%H:%M").timestamp()
                nowdate = datetime.now().timestamp()
                defdate=nowdate-lastdate
                prix = pricipal/actif
                newprix = prix * pow(1 + 0.001, 2) * pow(1 + 0.06 / (365 * 24 * 60 * 60), defdate)
                pourcentage=(pricipal+((float(actifprix)-newprix)*actif))/pricipal-1
                if 0.011<pourcentage:
                    if(executorder<4):
                        executorder+=1
                        if(actifprix<=self.sellprix):
                            self.db.updatedate()
                            buysell(self.client).sell(Socketio,order)
        user=self.db.get_portfolio_data()
        self.time=(datetime.now().timestamp()-datetime.strptime(user[self.date], "%Y-%m-%dT%H:%M").timestamp())
        if(12*60*60<self.time):
            buy=10
            nborder =float(user[enumsql.NBEXORDER.value])
            nborderdouble=float(user[enumsql.NBEXORDERDOUBLE.value])
            moneyprincipal= float(user[self.moneyprincipal])
            nborder=nborder+0.5 
            if(nborder<nborderdouble):
                nborderdouble=0
            if(512<nborder):
                nborderdouble=0
                nborder=0
            if(moneyprincipal/5<nborder):
                nborderdouble=0
                nborder=0
            newbuy=buy*pow(1.01,nborderdouble)
            if(newbuy<moneyprincipal):
                self.db.updatedate()
                quantite = newbuy/float(actifprix)
                res=spot(self.client).buy_market(quantite,actifprix)
                if res:
                    self.db.editportfolioorder(nborder,nborderdouble+1)
                    Socketio.emit("add",{
                        self.moneyprincipal:res[self.moneyprincipal],
                        self.moneyechange:res[self.moneyechange]
                    })
    def getsellprix(self):
        return self.sellprix
    def getbuytime(self):
        return str(timedelta(seconds=12*60*60-self.time))