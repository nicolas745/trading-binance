from flask import Flask, render_template, session, redirect, request
from chameleon import PageTemplate
from flask_socketio import SocketIO
from sql.trading import TradingDatabase
from classenum.env import configenv
from classenum.sql import enumsql
from apibinance.binance import Binance
from datetime import datetime
import os
class historique():
    def __init__(self,app:Flask,socket:SocketIO) -> None:
        self.app = app
        self.binance = Binance()
        self.socket = socket
        @app.get("/historique")
        def hist():
            #if(not session.get("user")):
            #    return redirect("/")
            pdate = request.args.get('pdate', datetime.now().strftime("%Y-%m-%d"))
            enddate = request.args.get('ldate', datetime.now().strftime("%Y-%m-%d"))
            args = {
                "data": self.binance.get_historique().gethistorique(datetime.strptime(pdate,"%Y-%m-%d").timestamp(),datetime.strptime(enddate,"%Y-%m-%d").timestamp()),
                "page" : "historique.html"
            }
            return self.misepage(**args)
    def misepage(self,**args):
        traide=TradingDatabase()
        spot = self.binance.get_spot().get_balances()
        args= args|{
            "orders":traide.get_all_orders(),
            configenv.MONEY_ECHANGE.name:os.getenv(configenv.MONEY_ECHANGE.value),
            configenv.MONEY_PRINCIPAL.name:os.getenv(configenv.MONEY_PRINCIPAL.value),
            "compte":traide.get_portfolio_data(),
            "wallet":{
                "spot":{
                        os.getenv(configenv.MONEY_ECHANGE.value):spot.getactifechange(),
                        os.getenv(configenv.MONEY_PRINCIPAL.value):spot.getactifprincal()
                },
                "earn":{
                }
            }
        }
        for name in enumsql._member_names_:
            args[name]= enumsql[name].value
        traide.close_connection()
        return PageTemplate(body=render_template("index_admin.html",**args)).render(**args)