from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(__name__)

# Use SQLite for simplicity in Replit environment
DB_PATH = 'angel2.db'

def init_db():
    """Initialize the database with schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Stock (
            stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_name VARCHAR(15) NOT NULL,
            stock_price INTEGER NOT NULL,
            pe_ratio INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Order" (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_name VARCHAR(15),
            quantity INTEGER,
            stock_id INTEGER,
            FOREIGN KEY (stock_id) REFERENCES Stock(stock_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Trader (
            dmat_account_number INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number VARCHAR(15),
            name VARCHAR(15) NOT NULL,
            mail_id VARCHAR(25),
            age INTEGER NOT NULL,
            order_id INTEGER,
            FOREIGN KEY (order_id) REFERENCES "Order"(order_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Futures_Options (
            fo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            type VARCHAR(7),
            contract_size INTEGER,
            underlying_asset INTEGER,
            expiry_date DATE,
            derivatives INTEGER,
            FOREIGN KEY (underlying_asset) REFERENCES Stock(stock_id),
            FOREIGN KEY (derivatives) REFERENCES Futures_Options(fo_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Broker (
            broker_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(15) NOT NULL,
            commission_rate DECIMAL(5,2) NOT NULL CHECK (commission_rate >= 0),
            license_number VARCHAR(15) UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS has_info (
            broker_id INTEGER,
            stock_id INTEGER,
            PRIMARY KEY (broker_id, stock_id),
            FOREIGN KEY (broker_id) REFERENCES Broker(broker_id) ON DELETE CASCADE,
            FOREIGN KEY (stock_id) REFERENCES Stock(stock_id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trader_order (
            trader_id INTEGER,
            order_id INTEGER,
            PRIMARY KEY (trader_id, order_id),
            FOREIGN KEY (trader_id) REFERENCES Trader(dmat_account_number) ON DELETE CASCADE,
            FOREIGN KEY (order_id) REFERENCES "Order"(order_id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phone_number (
            trader_id INTEGER,
            phone_number VARCHAR(15) NOT NULL,
            PRIMARY KEY (trader_id, phone_number),
            FOREIGN KEY (trader_id) REFERENCES Trader(dmat_account_number)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mail_id (
            trader_id INTEGER,
            mail_id VARCHAR(25) NOT NULL,
            PRIMARY KEY (trader_id, mail_id),
            FOREIGN KEY (trader_id) REFERENCES Trader(dmat_account_number)
        )
    ''')
    
    # Add sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM Stock")
    if cursor.fetchone()[0] == 0:
        sample_stocks = [
            ('RELIANCE', 2500, 25),
            ('TCS', 3200, 30),
            ('INFY', 1450, 22),
            ('HDFC', 1600, 20),
            ('ICICI', 950, 18)
        ]
        cursor.executemany(
            "INSERT INTO Stock (stock_name, stock_price, pe_ratio) VALUES (?, ?, ?)",
            sample_stocks
        )
    
    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Main page showing all tables"""
    return render_template('index.html')

@app.route('/stocks')
def stocks():
    """View all stocks"""
    conn = get_db()
    stocks = conn.execute('SELECT * FROM Stock').fetchall()
    conn.close()
    return render_template('stocks.html', stocks=stocks)

@app.route('/traders')
def traders():
    """View all traders"""
    conn = get_db()
    traders = conn.execute('SELECT * FROM Trader').fetchall()
    conn.close()
    return render_template('traders.html', traders=traders)

@app.route('/orders')
def orders():
    """View all orders"""
    conn = get_db()
    orders = conn.execute('SELECT * FROM "Order"').fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/brokers')
def brokers():
    """View all brokers"""
    conn = get_db()
    brokers = conn.execute('SELECT * FROM Broker').fetchall()
    conn.close()
    return render_template('brokers.html', brokers=brokers)

@app.route('/api/stocks')
def api_stocks():
    """API endpoint for stocks"""
    conn = get_db()
    stocks = conn.execute('SELECT * FROM Stock').fetchall()
    conn.close()
    return jsonify([dict(row) for row in stocks])

if __name__ == '__main__':
    # Initialize database
    if not os.path.exists(DB_PATH):
        init_db()
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)
