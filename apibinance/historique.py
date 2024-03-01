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
        spot = self.client.get_account_snapshot(type="SPOT", startTime=Pdate*1000,endTime=Ldate*1000)
        print(res)
        print("============================")
        print(spot)
        margin = self.client.get_account_snapshot(type="MARGIN", startTime=Pdate*1000,endTime=Ldate*1000)
        earn = self.client.get_account_snapshot(type="SAVINGS", startTime=Pdate*1000,endTime=Ldate*1000)
        return res