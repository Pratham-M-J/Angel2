# Angel2 - Stock Exchange Platform

## Overview
Angel2 is a comprehensive stock exchange platform database system that manages stocks, traders, orders, brokers, and futures & options trading. This project was imported from GitHub and has been configured to run in the Replit environment.

## Project Architecture

### Technology Stack
- **Backend**: Python 3.11 with Flask web framework (modular structure with blueprints)
- **Database**: MySQL (hosted at nzgz3x.h.filess.io)
- **Frontend**: HTML5 with embedded CSS (no separate build process needed)
- **Database Driver**: PyMySQL for MySQL connectivity

### File Structure
```
.
├── app.py                      # Main Flask application with blueprint registration
├── config.py                   # Database configuration
├── models.py                   # Database models (Stock, Trader, Order, Broker, F&O)
├── routes/                     # Route blueprints
│   ├── stock.py               # Stock management routes
│   ├── trader.py              # Trader management routes
│   ├── order.py               # Order placement routes
│   ├── broker.py              # Broker and stock listing routes
│   └── fo.py                  # Futures & Options routes
├── templates/                  # HTML templates
│   ├── index.html             # Homepage with all sections
│   ├── stocks.html            # Stock listings page
│   ├── traders.html           # Traders management page
│   ├── orders.html            # Orders viewing page
│   ├── order_place.html       # Order placement form
│   ├── brokers.html           # Brokers listing page
│   ├── broker_create.html     # Broker creation form
│   ├── broker_detail.html     # Broker details with stock listings
│   ├── fo_list.html           # Futures & Options listing
│   └── fo_create.html         # F&O creation form
├── 123.sql                     # Original MySQL schema
├── Angel2.sql                  # Additional schema file
├── schema.sql                  # PostgreSQL schema (reference, not used)
└── README.md                   # Project description
```

## Database Schema

The database includes the following tables:
1. **Stock** - Stock listings with prices and PE ratios
2. **Trader** - Trader accounts with DMAT information
3. **Order** - Buy/sell orders
4. **Broker** - Broker information and commission rates
5. **Futures_Options** - Futures and options contracts
6. **has_info** - Broker-Stock relationships
7. **trader_order** - Trader-Order relationships
8. **phone_number** - Trader phone numbers (multi-valued)
9. **mail_id** - Trader email addresses (multi-valued)

## Features
- **Stocks**: View and manage stock listings with pricing and PE ratios
- **Brokers**: Select brokers, view their stock listings, create new brokers with stock assignments
- **Traders**: Manage trader accounts with DMAT information
- **Orders**: Place orders for stocks or F&O contracts (buy/sell), view all orders
- **Futures & Options**: Create and manage F&O contracts linked to underlying assets
- Responsive web interface with modern gradient design
- Fully integrated with remote MySQL database

## Running the Application
The application automatically starts via the configured workflow:
- Server runs on port 5000
- Database connection to remote MySQL server at nzgz3x.h.filess.io
- Access the application through the Replit webview

## Development Notes
- Database password is securely stored in Replit Secrets (DB_PASSWORD environment variable)
- The application uses PyMySQL for MySQL connectivity
- All database operations use proper MySQL column names (with spaces and backticks)
- Modular architecture with Flask blueprints for better code organization

## Recent Changes (September 30, 2025)
- Restructured application with modular architecture (config, models, routes)
- Connected to remote MySQL database at nzgz3x.h.filess.io
- Implemented all required features: stocks, brokers, traders, orders, F&O
- Created comprehensive UI with broker selection, order placement (stock/F&O, buy/sell)
- Secured database credentials using environment variables
- Set up workflow to run on port 5000
- Created modern, responsive UI with gradient design
- Configured deployment settings for production with Gunicorn

## Original Project
This project was imported from a GitHub repository containing SQL database schemas for a stock exchange platform.
