from binance.client import Client
from datetime import datetime
from sql.trading import TradingDatabase
class historique:
    def __init__(self,client:Client) -> None:
        self.client = client
    def gethistorique(self,Pdate:float,Ldate:float):
        res = {}
        db = TradingDatabase()
        for i in range(int(Pdate),int(Ldate),60*60*24):
            res[datetime.utcfromtimestamp(i).strftime("%Y-%m-%d")] = db.gethistorique(i,self.client)
        return res