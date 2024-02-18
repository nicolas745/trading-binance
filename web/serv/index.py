from apibinance.spot import spot
from flask import Flask, render_template
class index():
    def __init__(self,app:Flask) -> None:
        @app.get("/")
        def auth():
            return render_template("index.html")