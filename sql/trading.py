import sqlite3
from datetime import datetime
import os
from classenum.env import configenv
from classenum.sql import enumsql
class TradingDatabase:
    def __init__(self, database_name='trading.db'):
        self.asset1 = os.getenv(configenv.MONEY_PRINCIPAL.value)
        self.asset2 = os.getenv(configenv.MONEY_ECHANGE.value)
        self.prix = enumsql.QUANTITEPRINCIPAL.value
        self.date = enumsql.DATE.value
        self.quantite = enumsql.QUANTITEACTIF.value
        self.capital_total = enumsql.CAPITAL_TOTAL.value
        self.conn = sqlite3.connect(database_name)
        self.create_tables()
        self.initialize_portfolio()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Table pour stocker le capital total et les quantités d'actifs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {} REAL,
                {} REAL,
                {} REAL
            )
        '''.format(self.capital_total,self.asset1,self.asset2))

        # Table pour stocker les ordres
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {} REAL,
                {} TEXT,
                {} REAL
            )
        '''.format(self.prix,self.date,self.quantite))
        self.conn.commit()

    def initialize_portfolio(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM portfolio')
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute('''
                INSERT INTO portfolio ({}, {}, {})
                VALUES (?, ?, ?)
            '''.format(self.capital_total,self.asset1,self.asset2), (0, 0, 0))
            self.conn.commit()

    def add_portfolio_data(self, capital_total, quantity_asset1, quantity_asset2):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE portfolio
            SET {} = ?, {} = ?, {} = ?
        '''.format(self.capital_total,capital_total, self.asset1), (quantity_asset1,self.asset2, quantity_asset2))
        self.conn.commit()

    def add_order(self, price, quantity,date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO orders ({}, {}, {})
            VALUES (?, ?, ?)
        '''.format(self.prix,self.date,self.quantite), (price, date, quantity))
        self.conn.commit()

    def delete_order(self, order_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM orders WHERE id = ?
        ''', (order_id,))
        self.conn.commit()

    def modify_order(self, order_id, new_price, new_quantity):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE orders SET {} = ?, {} = ? WHERE id = ?
        '''.format(self.prix,self.quantite), (new_price, new_quantity, order_id))
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