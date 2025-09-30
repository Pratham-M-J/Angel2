-- Stock Exchange Platform Database Schema (PostgreSQL)

CREATE TABLE IF NOT EXISTS Stock (
    stock_id SERIAL PRIMARY KEY,
    stock_name VARCHAR(15) NOT NULL,
    stock_price INTEGER NOT NULL,
    pe_ratio INTEGER
);

CREATE TABLE IF NOT EXISTS "Order" (
    order_id SERIAL PRIMARY KEY,
    stock_name VARCHAR(15),
    quantity INTEGER,
    stock_id INTEGER
);

CREATE TABLE IF NOT EXISTS Trader (
    dmat_account_number SERIAL PRIMARY KEY,
    phone_number VARCHAR(15),
    name VARCHAR(15) NOT NULL,
    mail_id VARCHAR(25),
    age INTEGER NOT NULL,
    order_id INTEGER
);

CREATE TABLE IF NOT EXISTS "Futures_Options" (
    fo_id SERIAL PRIMARY KEY,
    type VARCHAR(7),
    contract_size INTEGER,
    underlying_asset INTEGER,
    expiry_date DATE,
    derivatives INTEGER
);

CREATE TABLE IF NOT EXISTS Broker (
    broker_id SERIAL PRIMARY KEY,
    name VARCHAR(15) NOT NULL,
    commission_rate DECIMAL(5,2) NOT NULL CHECK (commission_rate >= 0),
    license_number VARCHAR(15) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS has_info (
    broker_id INTEGER,
    stock_id INTEGER,
    PRIMARY KEY (broker_id, stock_id)
);

CREATE TABLE IF NOT EXISTS trader_order (
    trader_id INTEGER,
    order_id INTEGER,
    PRIMARY KEY (trader_id, order_id)
);

CREATE TABLE IF NOT EXISTS phone_number (
    trader_id INTEGER,
    phone_number VARCHAR(15) NOT NULL,
    PRIMARY KEY (trader_id, phone_number)
);

CREATE TABLE IF NOT EXISTS mail_id (
    trader_id INTEGER,
    mail_id VARCHAR(25) NOT NULL,
    PRIMARY KEY (trader_id, mail_id)
);

-- Add Foreign Key Constraints
ALTER TABLE "Order"
ADD CONSTRAINT order_stockid
FOREIGN KEY (stock_id) REFERENCES Stock(stock_id);

ALTER TABLE Trader
ADD CONSTRAINT trader_orderid
FOREIGN KEY (order_id) REFERENCES "Order"(order_id);

ALTER TABLE "Futures_Options"
ADD CONSTRAINT derivative_of_derivative
FOREIGN KEY (derivatives) REFERENCES "Futures_Options"(fo_id);

ALTER TABLE "Futures_Options"
ADD CONSTRAINT underlying_asset
FOREIGN KEY (underlying_asset) REFERENCES Stock(stock_id);

ALTER TABLE has_info
ADD CONSTRAINT fk_hasinfo_broker FOREIGN KEY (broker_id)
    REFERENCES Broker(broker_id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE has_info
ADD CONSTRAINT fk_hasinfo_stock FOREIGN KEY (stock_id)
    REFERENCES Stock(stock_id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE trader_order
ADD CONSTRAINT fk_traderorder_trader FOREIGN KEY (trader_id)
    REFERENCES Trader(dmat_account_number)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE trader_order
ADD CONSTRAINT fk_traderorder_order FOREIGN KEY (order_id)
    REFERENCES "Order"(order_id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE phone_number
ADD CONSTRAINT fk_phone_trader FOREIGN KEY (trader_id)
    REFERENCES Trader(dmat_account_number);

ALTER TABLE mail_id
ADD CONSTRAINT fk_mail_trader FOREIGN KEY (trader_id)
    REFERENCES Trader(dmat_account_number);
