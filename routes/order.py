from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from models import Order, Stock, Trader, FuturesOptions, Broker

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders')
def list_orders():
    investments = Order.get_trader_investments()
    return render_template('orders.html', investments=investments)

@order_bp.route('/order/<int:order_id>')
def view_order(order_id):
    order = Order.get_by_id(order_id)
    return render_template('order_detail.html', order=order)

@order_bp.route('/order/place', methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        order_type = request.form.get('order_type')
        action = request.form.get('action')
        trader_id = request.form.get('trader_id')
        quantity = request.form.get('quantity')
        broker_id = request.form.get('broker_id')
        trader_id = request.form.get('trader_id')

        
        if order_type == 'stock':
            stock_id = request.form.get('stock_id')
            stock = Stock.get_by_id(stock_id)
            stock_name = stock['Stock Name'] if stock else ''
            
            order_id = Order.create(stock_name, quantity, stock_id, order_type='stock', action=action, broker_id=broker_id, trader_id=trader_id)
        elif order_type == 'fo':
            fo_id = request.form.get('fo_id')
            fo = FuturesOptions.get_by_id(fo_id)
            fo_name = f"{fo['Type']} Contract" if fo else ''
            
            order_id = Order.create(fo_name, quantity, fo_id, order_type='fo', action=action, broker_id=broker_id, trader_id=trader_id)
        Order.link_to_trader(trader_id,order_id)
        
        if action == 'sell':
            holdings = Order.get_trader_holdings(trader_id)
            if order_type == 'stock':
                stock_holding = next((s for s in holdings['stocks'] if s['name'] == stock_name), None)
                if not stock_holding or stock_holding['quantity'] < int(quantity):
                    flash('You do not have enough stocks to sell.', 'error')
                    return redirect(url_for('order.place_order'))
            elif order_type == 'fo':
                fo_holding = next((f for f in holdings['fos'] if f['name'] == fo_name), None)
                if not fo_holding or fo_holding['quantity'] < int(quantity):
                    flash('You do not have enough F&O contracts to sell.', 'error')
                    return redirect(url_for('order.place_order'))
        
        return redirect(url_for('order.list_orders'))
    
    stocks = Stock.get_all()
    traders = Trader.get_all()
    fos = FuturesOptions.get_all()
    brokers = Broker.get_all()
    return render_template('order_place.html', stocks=stocks, traders=traders, fos=fos, brokers=brokers)

@order_bp.route('/api/trader/<int:trader_id>/holdings')
def api_trader_holdings(trader_id):
    holdings = Order.get_trader_holdings(trader_id)
    return jsonify(holdings)

@order_bp.route('/trader/<int:trader_id>/orders')
def view_trader_orders(trader_id):
    orders = Order.get_orders_by_trader(trader_id)
    trader = Trader.get_by_id(trader_id)
    return render_template('trader_orders.html', orders=orders, trader=trader)
def api_orders():
    orders = Order.get_all()
    return jsonify([dict(order) for order in orders])
