from flask import Flask, session, redirect, render_template
from chameleon import PageTemplate
from apibinance.binance import Binance
class panel():
     def __init__(self,app:Flask) -> None:
          stream=Binance().get_stream()
          @app.get("/panel")
          def panel():
               if(not session.get("user")):
                    return redirect("/")
               return PageTemplate(body=render_template("panel.html")).render()
          @app.get("/order")
          def order():
               if(not session.get("user")):
                    return redirect("/")
               return PageTemplate(body=render_template("order.html")).render()