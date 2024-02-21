from sql.trading import TradingDatabase
from classenum.sql import enumsql
from classenum.env import configenv
from datetime import datetime
from binance.client import AsyncClient

class bot:
    def __init__(self, data, db:TradingDatabase,client:AsyncClient) -> None:
        self.db = db
        self.client = client
        self.data = {}
        self.data['time'] = data["T"]/1000
        self.data["prix"] = data["p"]
        print(data)

    def start(self):
        orders = self.db.get_all_orders()
        for order in orders:
            date_time_object = datetime.strptime(order[enumsql.DATE.value], "%Y-%m-%dT%H:%M")
            timestamp = date_time_object.timestamp()
            timedif = self.data['time'] - timestamp
            prix = order[enumsql.QUANTITEACTIF.value] / order[enumsql.QUANTITEPRINCIPAL.value]
            calcprix = prix * pow(1 + 0.05 / (365 * 24 * 60 * 60), timedif)
            calcprix, float(self.data["prix"]), float(self.data["prix"]) / calcprix
        print(self.client.get_simple_earn_account(),self.client.API_KEY,self.client.API_SECRET)
        exit()
