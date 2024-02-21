from flask import Flask, session, redirect, render_template
from chameleon import PageTemplate
from flask_socketio import SocketIO
import os
from classenum.env import configenv
from apibinance.binance import Binance
from sql.trading import TradingDatabase
class panel():
     def __init__(self,app:Flask,socket:SocketIO) -> None:
          #stream=Binance().get_stream(socketio=socket)
          @app.get("/panel")
          def panel():
               if(not session.get("user")):
                    return redirect("/")
               args = {
                    "page":"panel.html"
               }
               return self.misepage(**args)
          @app.get("/order")
          def order():
               if(not session.get("user")):
                    return redirect("/")
               args={
                    "page":"order.html",
               }
               return self.misepage(**args)
     def misepage(self,**args):
          traide=TradingDatabase()
          data=traide.get_portfolio_data()
          print(data)
          args= args|{
               "ordes":[],
               configenv.MONEY_ECHANGE.name:os.getenv(configenv.MONEY_ECHANGE.value),
               configenv.MONEY_PRINCIPAL.name:os.getenv(configenv.MONEY_PRINCIPAL.value),
               "compte":traide.get_portfolio_data()
          }
          traide.close_connection()
          return PageTemplate(body=render_template("index_admin.html",**args)).render(**args)