import sqlite3
from datetime import datetime
import os
from classenum.env import configenv
from classenum.sql import enumsql
class TradingDatabase:
    def __init__(self, database_name='trading.db'):
        self.asset1 = os.getenv(configenv.MONEY_PRINCIPAL.value)
        self.asset2 = os.getenv(configenv.MONEY_ECHANGE.value)
        self.ordertime= enumsql.ORDERTIME.value
        self.quantitepricipal = enumsql.QUANTITEPRINCIPAL.value
        self.date = enumsql.DATE.value
        self.quantite = enumsql.QUANTITEACTIF.value
        self.capital_total = enumsql.CAPITAL_TOTAL.value
        self.conn = sqlite3.connect(database_name)
        self.create_tables()
        self.initialize_portfolio()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {} REAL,
                {} REAL,
                {} REAL,
                {} TEXT
            )
        '''.format(self.capital_total,self.asset1,self.asset2,self.ordertime))
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {} REAL,
                {} TEXT,
                {} REAL
            )
        '''.format(self.quantitepricipal,self.date,self.quantite))
        self.conn.commit()

    def initialize_portfolio(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM portfolio')
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute('''
                INSERT INTO portfolio ({}, {}, {},{})
                VALUES (?, ?, ?,?)
            '''.format(self.capital_total,self.asset1,self.asset2,self.ordertime), (0, 0, 0,datetime.now().strftime("%Y-%m-%dT%H:%M")))
            self.conn.commit()

    def edit_portfolio_data(self,ordertime):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE portfolio
            SET {}=?
        '''.format(self.ordertime), (ordertime))
        self.conn.commit()
    def edit_portfolio(self, capital_total, asset1, asset2,ordertime):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE portfolio
            SET {} = ?, {} = ?, {} = ?, {} = ? 
        '''.format(self.capital_total, self.asset1, self.asset2, self.ordertime), (capital_total, asset1, asset2,ordertime))
        self.conn.commit()
    def add_order(self, quantity1, quantity2,date=datetime.now().strftime("%Y-%m-%dT%H:%M")):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO orders ({}, {}, {})
            VALUES (?, ?, ?)
        '''.format(self.quantitepricipal,self.date,self.quantite), (quantity1, date, quantity2))
        portfolio=self.get_portfolio_data()
        if float(datetime.strptime(portfolio[enumsql.DATE.value],"%Y-%m-%dT%H:%M").timestamp())<float(datetime.strptime(date,"%Y-%m-%dT%H:%M").timestamp()):
            self.edit_portfolio_data(date)
        self.conn.commit()
    def delete_order(self, order_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM orders WHERE id = ?
        ''', (order_id,))
        self.conn.commit()

    def modify_order(self, order_id, new_quantitypri, new_quantity):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE orders SET {} = ?, {} = ? WHERE id = ?
        '''.format(self.quantitepricipal,self.quantite), (new_quantitypri, new_quantity, order_id))
        self.conn.commit()
    def close_connection(self):
        self.conn.close()

    def get_portfolio_data(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM portfolio')
        result = cursor.fetchone()
        if result:
            # Créer un dictionnaire avec les noms de colonnes comme clés
            columns = [col[0] for col in cursor.description]
            portfolio_dict = dict(zip(columns, result))
            return portfolio_dict
        else:
            return None
    def get_order(self,orderid):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE id=?',(orderid))
        results = cursor.fetchall()
        if results:
            # Créer une liste de dictionnaires pour chaque ligne
            columns = [col[0] for col in cursor.description]
            orders_list = [dict(zip(columns, row)) for row in results]
            return orders_list
        else:
            return []
    def get_all_orders(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM orders')
        results = cursor.fetchall()

        if results:
            # Créer une liste de dictionnaires pour chaque ligne
            columns = [col[0] for col in cursor.description]
            orders_list = [dict(zip(columns, row)) for row in results]
            return orders_list
        else:
            return []