import sqlite3
from datetime import datetime

class TradingDatabase:
    def __init__(self, database_name='trading.db'):
        self.conn = sqlite3.connect(database_name)
        self.create_tables()
        self.initialize_portfolio()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Table pour stocker le capital total et les quantités d'actifs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                capital_total REAL,
                quantity_asset1 REAL,
                quantity_asset2 REAL
            )
        ''')

        # Table pour stocker les ordres
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                price REAL,
                date TEXT,
                quantity REAL,
                asset_id INTEGER,
                FOREIGN KEY(asset_id) REFERENCES portfolio(id)
            )
        ''')

        self.conn.commit()

    def initialize_portfolio(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM portfolio')
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute('''
                INSERT INTO portfolio (capital_total, quantity_asset1, quantity_asset2)
                VALUES (?, ?, ?)
            ''', (0, 0, 0))
            self.conn.commit()

    def add_portfolio_data(self, capital_total, quantity_asset1, quantity_asset2):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE portfolio
            SET capital_total = ?, quantity_asset1 = ?, quantity_asset2 = ?
        ''', (capital_total, quantity_asset1, quantity_asset2))
        self.conn.commit()
    def create_tables(self):
        cursor = self.conn.cursor()

        # Table pour stocker le capital total et les quantités d'actifs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                capital_total REAL,
                quantity_asset1 REAL,
                quantity_asset2 REAL
            )
        ''')

        # Table pour stocker les ordres
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                price REAL,
                date TEXT,
                quantity REAL,
                asset_id INTEGER,
                FOREIGN KEY(asset_id) REFERENCES portfolio(id)
            )
        ''')

        self.conn.commit()

    def add_portfolio_data(self, capital_total, quantity_asset1, quantity_asset2):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO portfolio (capital_total, quantity_asset1, quantity_asset2)
            VALUES (?, ?, ?)
        ''', (capital_total, quantity_asset1, quantity_asset2))
        self.conn.commit()

    def add_order(self, price, quantity, asset_id):
        cursor = self.conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO orders (price, date, quantity, asset_id)
            VALUES (?, ?, ?, ?)
        ''', (price, date, quantity, asset_id))
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
            UPDATE orders SET price = ?, quantity = ? WHERE id = ?
        ''', (new_price, new_quantity, order_id))
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