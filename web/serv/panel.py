from flask import Flask, session, redirect
class panel():
     def __init__(self,app:Flask) -> None:
          @app.get("/panel")
          def panel():
               if(not session.get("user")):
                    return redirect("/")
               return "dd"
          @app.get("/order")
          def order():
               if(not session.get("user")):
                    return redirect("/")
               return "dd"