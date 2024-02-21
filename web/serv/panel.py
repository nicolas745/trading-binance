from flask import Flask, session, redirect, render_template,request
from chameleon import PageTemplate
from flask_socketio import SocketIO
import os
from classenum.env import configenv
from apibinance.binance import Binance
from classenum.sql import enumsql
from sql.trading import TradingDatabase
class panel():
     def __init__(self,app:Flask,socket:SocketIO) -> None:
          self.stream=Binance().get_stream(socketio=socket)
          @app.get("/panel")
          def panel():
               if(not session.get("user")):
                    return redirect("/")
               args = {
                    "page":"panel.html"
               }
               return self.misepage(**args)
          @app.post("/order")
          def getorder():
               trading=TradingDatabase()
               if(request.form.get("add")):
                    trading.add_order(
                         request.form.get(enumsql.QUANTITEACTIF.value),
                         request.form.get(enumsql.QUANTITEPRINCIPAL.value)
                    )
               args={
                    "page":"order.html",
               }
               trading.close_connection()
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
          args= args|{
               "orders":traide.get_all_orders(),
               configenv.MONEY_ECHANGE.name:os.getenv(configenv.MONEY_ECHANGE.value),
               configenv.MONEY_PRINCIPAL.name:os.getenv(configenv.MONEY_PRINCIPAL.value),
               "compte":traide.get_portfolio_data(),
               enumsql.CAPITAL_TOTAL.name:enumsql.CAPITAL_TOTAL.value
          }|self.stream.getdata()
          for name in enumsql._member_names_:
               args[name]= enumsql[name].value
          traide.close_connection()
          return PageTemplate(body=render_template("index_admin.html",**args)).render(**args)