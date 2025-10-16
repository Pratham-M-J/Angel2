# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## High-Level Architecture

This is a Flask-based web application that serves as a stock exchange platform. The backend is written in Python 3.11, and it uses a modular structure with Flask Blueprints to organize routes. The database is MySQL, and the application connects to it using PyMySQL. The frontend is built with HTML5 and embedded CSS.

- **`app.py`**: The main entry point of the Flask application. It registers the blueprints for different modules.
- **`config.py`**: Contains the database configuration. The database password is read from the `DB_PASSWORD` environment variable.
- **`models.py`**: Defines the database models for entities like `Stock`, `Trader`, `Order`, `Broker`, and `Futures_Options`.
- **`routes/`**: This directory contains the Flask Blueprints for different parts of the application:
    - `stock.py`: Routes for managing stocks.
    - `trader.py`: Routes for managing traders.
    - `order.py`: Routes for placing and viewing orders.
    - `broker.py`: Routes for managing brokers and their stock listings.
    - `fo.py`: Routes for managing futures and options.
- **`templates/`**: This directory contains the HTML templates for the frontend.

## Common Commands

- **To run the development server**:
  ```bash
  python app.py
  ```
  The application will be available at `http://localhost:5000`.

- **Database**: The application connects to a remote MySQL database. The connection details are in `config.py`, and the password should be set as an environment variable `DB_PASSWORD`.
