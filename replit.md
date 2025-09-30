# Angel2 - Stock Exchange Platform

## Overview
Angel2 is a comprehensive stock exchange platform database system that manages stocks, traders, orders, brokers, and futures & options trading. This project was imported from GitHub and has been configured to run in the Replit environment.

## Project Architecture

### Technology Stack
- **Backend**: Python 3.11 with Flask web framework
- **Database**: SQLite (for development ease in Replit)
- **Frontend**: HTML5 with embedded CSS (no separate build process needed)

### File Structure
```
.
├── app.py                 # Main Flask application
├── schema.sql            # PostgreSQL schema (reference)
├── angel2.db             # SQLite database (auto-generated)
├── templates/            # HTML templates
│   ├── index.html       # Landing page
│   ├── stocks.html      # Stock listings page
│   ├── traders.html     # Traders management page
│   ├── orders.html      # Orders tracking page
│   └── brokers.html     # Brokers information page
├── 123.sql              # Original MySQL schema
├── Angel2.sql           # Additional schema file
└── README.md            # Project description
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
- View stock listings with real-time pricing
- Manage trader accounts
- Track orders
- Monitor broker information
- Responsive web interface with modern design

## Running the Application
The application automatically starts via the configured workflow:
- Server runs on port 5000
- Database is automatically initialized with sample data on first run
- Access the application through the Replit webview

## Development Notes
- Sample data is automatically loaded for demonstration purposes
- The application uses SQLite instead of PostgreSQL/MySQL for simplicity in the Replit environment
- All database operations are handled through SQLite3 Python library

## Recent Changes (September 30, 2025)
- Converted MySQL schema to SQLite-compatible format
- Created Flask web application for database interaction
- Set up workflow to run on port 5000
- Added sample stock data for demonstration
- Created modern, responsive UI with gradient design
- Configured deployment settings for production

## Original Project
This project was imported from a GitHub repository containing SQL database schemas for a stock exchange platform.
