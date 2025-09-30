from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import Order, Stock, Trader, FuturesOptions

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders')
def list_orders():
    orders = Order.get_all()
    return render_template('orders.html', orders=orders)

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
        
        if order_type == 'stock':
            stock_id = request.form.get('stock_id')
            stock = Stock.get_by_id(stock_id)
            stock_name = stock['Stock Name'] if stock else ''
            
            order_id = Order.create(stock_name, quantity, stock_id, order_type='stock')
        elif order_type == 'fo':
            fo_id = request.form.get('fo_id')
            fo = FuturesOptions.get_by_id(fo_id)
            fo_name = f"{fo['Type']} Contract" if fo else ''
            
            order_id = Order.create(fo_name, quantity, fo_id, order_type='fo')
        
        if trader_id:
            Order.link_to_trader(trader_id, order_id)
        
        return redirect(url_for('order.list_orders'))
    
    stocks = Stock.get_all()
    traders = Trader.get_all()
    fos = FuturesOptions.get_all()
    return render_template('order_place.html', stocks=stocks, traders=traders, fos=fos)

@order_bp.route('/api/orders')
def api_orders():
    orders = Order.get_all()
    return jsonify([dict(order) for order in orders])
