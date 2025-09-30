import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def get_db_connection():
    """Get database connection"""
    conn = psycopg2.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT
    )
    return conn

def get_db_cursor(conn):
    """Get database cursor with RealDictCursor"""
    return conn.cursor(cursor_factory=RealDictCursor)

class Stock:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = get_db_cursor(conn)
        cursor.execute('SELECT * FROM Stock')
        stocks = cursor.fetchall()
        conn.close()
        return stocks
    
    @staticmethod
    def get_by_id(stock_id):
        conn = get_db_connection()
        cursor = get_db_cursor(conn)
        cursor.execute('SELECT * FROM Stock WHERE stock_id = %s', (stock_id,))
        stock = cursor.fetchone()
        conn.close()
        return stock
    
    @staticmethod
    def create(stock_name, stock_price, pe_ratio):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Stock (stock_name, stock_price, pe_ratio) VALUES (%s, %s, %s) RETURNING stock_id',
            (stock_name, stock_price, pe_ratio)
        )
        stock_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return stock_id

class Trader:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = get_db_cursor(conn)
        cursor.execute('SELECT * FROM Trader')
        traders = cursor.fetchall()
        conn.close()
        return traders
    
    @staticmethod
    def get_by_id(dmat_account_number):
        conn = get_db_connection()
        cursor = get_db_cursor(conn)
        cursor.execute('SELECT * FROM Trader WHERE dmat_account_number = %s', (dmat_account_number,))
        trader = cursor.fetchone()
        conn.close()
        return trader
    
    @staticmethod
    def create(name, age, phone_number=None, mail_id=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Trader (name, age, phone_number, mail_id) VALUES (%s, %s, %s, %s) RETURNING dmat_account_number',
            (name, age, phone_number, mail_id)
        )
        dmat_account_number = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return dmat_account_number

class Order:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = get_db_cursor(conn)
        cursor.execute('SELECT * FROM "Order"')
        orders = cursor.fetchall()
        conn.close()
        return orders
    
    @staticmethod
    def get_by_id(order_id):
        conn = get_db_connection()
        cursor = get_db_cursor(conn)
        cursor.execute('SELECT * FROM "Order" WHERE order_id = %s', (order_id,))
        order = cursor.fetchone()
        conn.close()
        return order
    
    @staticmethod
    def create(stock_name, quantity, stock_id, order_type='stock'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO "Order" (stock_name, quantity, stock_id) VALUES (%s, %s, %s) RETURNING order_id',
            (stock_name, quantity, stock_id)
        )
        order_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return order_id
    
    @staticmethod
    def link_to_trader(trader_id, order_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO trader_order (trader_id, order_id) VALUES (%s, %s)',
            (trader_id, order_id)
        )
        conn.commit()
        conn.close()

class Broker:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = get_db_cursor(conn)
        cursor.execute('SELECT * FROM Broker')
        brokers = cursor.fetchall()
        conn.close()
        return brokers
    
    @staticmethod
    def get_by_id(broker_id):
        conn = get_db_connection()
        cursor = get_db_cursor(conn)
        cursor.execute('SELECT * FROM Broker WHERE broker_id = %s', (broker_id,))
        broker = cursor.fetchone()
        conn.close()
        return broker
    
    @staticmethod
    def create(name, commission_rate, license_number):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Broker (name, commission_rate, license_number) VALUES (%s, %s, %s) RETURNING broker_id',
            (name, commission_rate, license_number)
        )
        broker_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return broker_id
    
    @staticmethod
    def get_stocks(broker_id):
        conn = get_db_connection()
        cursor = get_db_cursor(conn)
        cursor.execute('''
            SELECT s.* FROM Stock s
            JOIN has_info hi ON s.stock_id = hi.stock_id
            WHERE hi.broker_id = %s
        ''', (broker_id,))
        stocks = cursor.fetchall()
        conn.close()
        return stocks
    
    @staticmethod
    def add_stock(broker_id, stock_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO has_info (broker_id, stock_id) VALUES (%s, %s)',
            (broker_id, stock_id)
        )
        conn.commit()
        conn.close()

class FuturesOptions:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = get_db_cursor(conn)
        cursor.execute('SELECT * FROM Futures_Options')
        fos = cursor.fetchall()
        conn.close()
        return fos
    
    @staticmethod
    def get_by_id(fo_id):
        conn = get_db_connection()
        cursor = get_db_cursor(conn)
        cursor.execute('SELECT * FROM Futures_Options WHERE fo_id = %s', (fo_id,))
        fo = cursor.fetchone()
        conn.close()
        return fo
    
    @staticmethod
    def create(fo_type, contract_size, underlying_asset, expiry_date, derivatives=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Futures_Options (type, contract_size, underlying_asset, expiry_date, derivatives) VALUES (%s, %s, %s, %s, %s) RETURNING fo_id',
            (fo_type, contract_size, underlying_asset, expiry_date, derivatives)
        )
        fo_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return fo_id
