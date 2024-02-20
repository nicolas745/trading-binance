from flask import Flask, session, redirect, render_template
from chameleon import PageTemplate
import binance
import time
import threading
class panel():
     def __init__(self,app:Flask) -> None:
          t= threading.Thread(target=self.live)
          t.start()
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
     def live(self):
          while True:
               time.sleep(60)
               pass