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
        prix = {}
        for i in range(int(Pdate),int(Ldate),60*60*24):
            if(i in res.keys()):
                if i in prix.keys():
                    reqprixs=self.client.get_historical_klines(symbol="BTCUSDT",start_str=i,limit=500)
                    for i2 in range(0,499,1):
                        prix[Pdate+i2*60*60*249]=reqprixs[i2][1] 
                spot = self.client.get_account_snapshot(type="SPOT", startTime=int(Pdate*1000),limit=500,endTime=int(Ldate*1000))
                margin = self.client.get_account_snapshot(type="MARGIN", sstartTime=int(Pdate*1000),limit=500,endTime=int(Ldate*1000))
                
        return res