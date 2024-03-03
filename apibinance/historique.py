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
            date = datetime.utcfromtimestamp(i).strftime("%Y-%m-%d")
            sql =db.gethistorique(i,self.client)
            if sql:
                res[date] = sql
        spot = self.client.get_account_snapshot(type="SPOT", startTime=int(Pdate*1000),limit=500)
        print(res)
        print("============================")
        print(spot)
        margin = self.client.get_account_snapshot(type="MARGIN", sstartTime=int(Pdate*1000),limit=500)
        earn = self.client.get_account_snapshot(type="SAVINGS", startTime=int(Pdate*1000),limit=500)
        return res