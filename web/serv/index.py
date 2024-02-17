from apibinance.spot import spot
from flask import Flask
class index():
    def __init__(self,app:Flask) -> None:
        @app.get("/")
        def auth():
            return "d"