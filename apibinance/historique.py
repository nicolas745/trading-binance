from binance.client import Client
from datetime import datetime, timedelta
from classenum.sql import enumsql
from sql.trading import TradingDatabase

class historique:
    def __init__(self, client: Client) -> None:
        self.client = client
    def gethistorique(self, Pdate: float, Ldate: float):
        db = TradingDatabase()
        sql = db.gethistorique(Pdate, Ldate, self.client)

        # Convert dates to datetime
        dates_sql = [datetime.fromtimestamp(float(row[enumsql.DATE.value])) for row in sql]

        # Generate all possible dates between Pdate and Ldate
        start_date = datetime.fromtimestamp(Pdate)
        end_date = datetime.fromtimestamp(Ldate)
        all_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        # Find missing dates
        missing_dates = [date for date in all_dates if date not in dates_sql]

        # Display missing dates
        if missing_dates:
            print("Missing dates:", missing_dates)
        
        return sql
