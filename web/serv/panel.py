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
          self.binance = Binance()
          self.stream=self.binance.get_stream(socketio=socket)
          self.stream.start()
          @app.get("/panel")
          def getpanel():
               if(not session.get("user")):
                    return redirect("/")
               args = {
                    "page":"panel.html"
               }
               return self.misepage(**args)
          @app.post("/panel")
          def postpanel():
               if(request.form.get("submit")):
                    trading=TradingDatabase()
                    trading.edit_portfolio(
                         request.form.get(os.getenv(configenv.MONEY_PRINCIPAL.value)),
                         request.form.get(os.getenv(configenv.MONEY_ECHANGE.value)),
                    )
                    trading.close_connection()
               if(not session.get("user")):
                    return redirect("/")
               args = {
                    "page":"panel.html"
               }
               return self.misepage(**args)
          @app.get("/<idorder>/edit")
          def getedit(idorder):
               if(not session.get("user")):
                    return redirect("/")
               args = {
                    "page":"edit.html"
               }
               return self.misepage(**args)
          @app.post("/<idorder>/edit")
          def postedit(idorder):
               if(not session.get("user")):
                    return redirect("/")
               if(request.form.get("add")):
                   trading=TradingDatabase()
                   trading.modify_order(
                         idorder,
                         request.form.get(os.getenv(configenv.MONEY_PRINCIPAL.value)),
                         request.form.get(os.getenv(configenv.MONEY_ECHANGE.value)),
                    ) 
                   trading.close_connection()
               if(not session.get("user")):
                    return redirect("/")
               args = {
                    "page":"edit.html"
               }
               return self.misepage(**args)
          @app.post("/order")
          def postorder():
               if(not session.get("user")):
                    return redirect("/")
               trading=TradingDatabase()
               if(request.form.get("add")):
                    trading.add_order(
                         request.form.get(os.getenv(configenv.MONEY_PRINCIPAL.value)),
                         request.form.get(os.getenv(configenv.MONEY_ECHANGE.value)),
                         request.form.get(enumsql.DATE.value)
                    )
               if(request.form.get("buy")):
                    self.binance.get_spot().buy_market(request.form.get(os.getenv(configenv.MONEY_ECHANGE.value)),self.stream.getprix())
               if(request.form.get("edit")):
                    return redirect("/"+request.form.get("edit")+"/edit")
               if(request.form.get("sell")):
                    self.binance.get_spot().sell_market(request.form.get("sell"))
               if(request.form.get("del")):
                    trading.delete_order(request.form.get("del"))
               args={
                    "page":"order.html",
               }
               trading.close_connection()
               return self.misepage(**args)
          @app.get("/order")
          def getorder():
               if(not session.get("user")):
                    return redirect("/")
               if(not session.get("user")):
                    return redirect("/")
               args={
                    "page":"order.html",
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
               "sellprix":self.stream.getsellprix(),
               "prixact" : self.stream.getprix(),
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