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
        print("Stock ID is: ", stock_id)
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
        # Ensure phone_number is an integer
        if phone_number:
            try:
                phone_number = int(phone_number)
            except (ValueError, TypeError):
                phone_number = None  # Or handle the error as you see fit

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
    def create(stock_name, quantity, stock_id, order_type='stock', action='buy', broker_id=None, trader_id=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO `Order` (`Stock Name`, Quantity, `Stock ID`, `Order Type`, action, BrokerID, `Trader ID`) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (stock_name, quantity, stock_id, order_type, action, broker_id, trader_id)
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

    @staticmethod
    def get_trader_investments():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                t.Name AS trader_name,
                t.`DMAT Account Number` AS trader_id,
                COALESCE(SUM(
                    CASE
                        WHEN o.`Order Type` = 'stock' AND o.action = 'buy' THEN o.Quantity * s.`Stock Price`
                        WHEN o.`Order Type` = 'stock' AND o.action = 'sell' THEN -o.Quantity * s.`Stock Price`
                        WHEN o.`Order Type` = 'fo' AND o.action = 'buy' THEN o.Quantity * fo.`Contract Size` * s_fo.`Stock Price`
                        WHEN o.`Order Type` = 'fo' AND o.action = 'sell' THEN -o.Quantity * fo.`Contract Size` * s_fo.`Stock Price`
                        ELSE 0
                    END
                ), 0) AS total_investment
            FROM
                Trader t
            LEFT JOIN
                trader_order tor ON t.`DMAT Account Number` = tor.`trader id`
            LEFT JOIN
                `Order` o ON tor.`order id` = o.`Order ID`
            LEFT JOIN
                Stock s ON o.`Stock ID` = s.`Stock ID` AND o.`Order Type` = 'stock'
            LEFT JOIN
                `Futures & Options` fo ON o.`Stock ID` = fo.`F&O ID` AND o.`Order Type` = 'fo'
            LEFT JOIN
                Stock s_fo ON fo.`Underlying Asset` = s_fo.`Stock ID`
            GROUP BY
                t.`DMAT Account Number`, t.Name
        ''')
        investments = cursor.fetchall()
        conn.close()
        return investments

    @staticmethod
    def get_orders_by_trader(trader_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                o.`Order ID`,
                o.`Order Type`,
                o.action,
                o.Quantity AS quantity,
                o.`Stock Name` AS stock_name,
                b.Name AS broker_name,
                CASE
                    WHEN o.`Order Type` = 'stock' THEN s.`Stock Price`
                    WHEN o.`Order Type` = 'fo' THEN s_fo.`Stock Price`
                END AS price,
                CASE
                    WHEN o.`Order Type` = 'stock' AND o.action = 'buy' THEN o.Quantity * s.`Stock Price`
                    WHEN o.`Order Type` = 'stock' AND o.action = 'sell' THEN -o.Quantity * s.`Stock Price`
                    WHEN o.`Order Type` = 'fo' AND o.action = 'buy' THEN o.Quantity * fo.`Contract Size` * s_fo.`Stock Price`
                    WHEN o.`Order Type` = 'fo' AND o.action = 'sell' THEN -o.Quantity * fo.`Contract Size` * s_fo.`Stock Price`
                    ELSE 0
                END AS total_investment
            FROM
                `Order` o
            JOIN
                trader_order tor ON o.`Order ID` = tor.`order id`
            LEFT JOIN
                Broker b ON o.BrokerID = b.BrokerID
            LEFT JOIN
                Stock s ON o.`Stock ID` = s.`Stock ID` AND o.`Order Type` = 'stock'
            LEFT JOIN
                `Futures & Options` fo ON o.`Stock ID` = fo.`F&O ID` AND o.`Order Type` = 'fo'
            LEFT JOIN
                Stock s_fo ON fo.`Underlying Asset` = s_fo.`Stock ID`
            WHERE
                tor.`trader id` = %s
        ''', (trader_id,))
        orders = cursor.fetchall()
        conn.close()
        return orders

    @staticmethod
    def get_trader_holdings(trader_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Get stock holdings
        cursor.execute('''
            SELECT
                s.`Stock Name` AS name,
                SUM(CASE WHEN o.action = 'buy' THEN o.Quantity ELSE -o.Quantity END) AS quantity
            FROM `Order` o
            JOIN trader_order tor ON o.`Order ID` = tor.`order id`
            JOIN Stock s ON o.`Stock ID` = s.`Stock ID`
            WHERE tor.`trader id` = %s AND o.`Order Type` = 'stock'
            GROUP BY s.`Stock Name`
        ''', (trader_id,))
        stocks = cursor.fetchall()

        # Get F&O holdings
        cursor.execute('''
            SELECT
                fo.Type AS name,
                SUM(CASE WHEN o.action = 'buy' THEN o.Quantity ELSE -o.Quantity END) AS quantity
            FROM `Order` o
            JOIN trader_order tor ON o.`Order ID` = tor.`order id`
            JOIN `Futures & Options` fo ON o.`Stock ID` = fo.`F&O ID`
            WHERE tor.`trader id` = %s AND o.`Order Type` = 'fo'
            GROUP BY fo.Type
        ''', (trader_id,))
        fos = cursor.fetchall()

        conn.close()
        return {"stocks": stocks, "fos": fos}

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
