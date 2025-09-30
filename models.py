import pymysql
import pymysql.cursors
from config import Config

def get_db_connection():
    """Get database connection"""
    conn = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT,
        charset=Config.DB_CHARSET,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

class Stock:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Stock')
        stocks = cursor.fetchall()
        conn.close()
        return stocks
    
    @staticmethod
    def get_by_id(stock_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Stock WHERE `Stock ID` = %s', (stock_id,))
        stock = cursor.fetchone()
        conn.close()
        return stock
    
    @staticmethod
    def create(stock_name, stock_price, pe_ratio):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Stock (`Stock Name`, `Stock Price`, `PE Ratio`) VALUES (%s, %s, %s)',
            (stock_name, stock_price, pe_ratio)
        )
        stock_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return stock_id

class Trader:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Trader')
        traders = cursor.fetchall()
        conn.close()
        return traders
    
    @staticmethod
    def get_by_id(dmat_account_number):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Trader WHERE `DMAT Account Number` = %s', (dmat_account_number,))
        trader = cursor.fetchone()
        conn.close()
        return trader
    
    @staticmethod
    def create(name, age, phone_number=None, mail_id=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Trader (Name, Age, `Phone Number`, `Mail ID`) VALUES (%s, %s, %s, %s)',
            (name, age, phone_number, mail_id)
        )
        dmat_account_number = cursor.lastrowid
        conn.commit()
        conn.close()
        return dmat_account_number

class Order:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM `Order`')
        orders = cursor.fetchall()
        conn.close()
        return orders
    
    @staticmethod
    def get_by_id(order_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM `Order` WHERE `Order ID` = %s', (order_id,))
        order = cursor.fetchone()
        conn.close()
        return order
    
    @staticmethod
    def create(stock_name, quantity, stock_id, order_type='stock'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO `Order` (`Stock Name`, Quantity, `Stock ID`) VALUES (%s, %s, %s)',
            (stock_name, quantity, stock_id)
        )
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return order_id
    
    @staticmethod
    def link_to_trader(trader_id, order_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO trader_order (`trader id`, `order id`) VALUES (%s, %s)',
            (trader_id, order_id)
        )
        conn.commit()
        conn.close()

class Broker:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Broker')
        brokers = cursor.fetchall()
        conn.close()
        return brokers
    
    @staticmethod
    def get_by_id(broker_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Broker WHERE BrokerID = %s', (broker_id,))
        broker = cursor.fetchone()
        conn.close()
        return broker
    
    @staticmethod
    def create(name, commission_rate, license_number):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Broker (Name, CommissionRate, LicenseNumber) VALUES (%s, %s, %s)',
            (name, commission_rate, license_number)
        )
        broker_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return broker_id
    
    @staticmethod
    def get_stocks(broker_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.* FROM Stock s
            JOIN has_info hi ON s.`Stock ID` = hi.`Stock ID`
            WHERE hi.BrokerID = %s
        ''', (broker_id,))
        stocks = cursor.fetchall()
        conn.close()
        return stocks
    
    @staticmethod
    def add_stock(broker_id, stock_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO has_info (BrokerID, `Stock ID`) VALUES (%s, %s)',
            (broker_id, stock_id)
        )
        conn.commit()
        conn.close()

class FuturesOptions:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM `Futures & Options`')
        fos = cursor.fetchall()
        conn.close()
        return fos
    
    @staticmethod
    def get_by_id(fo_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM `Futures & Options` WHERE `F&O ID` = %s', (fo_id,))
        fo = cursor.fetchone()
        conn.close()
        return fo
    
    @staticmethod
    def create(fo_type, contract_size, underlying_asset, expiry_date, derivatives=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO `Futures & Options` (Type, `Contract Size`, `Underlying Asset`, `Expiry Date`, Derivates) VALUES (%s, %s, %s, %s, %s)',
            (fo_type, contract_size, underlying_asset, expiry_date, derivatives)
        )
        fo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return fo_id
