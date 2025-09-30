from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import Broker, Stock

broker_bp = Blueprint('broker', __name__)

@broker_bp.route('/brokers')
def list_brokers():
    brokers = Broker.get_all()
    return render_template('brokers.html', brokers=brokers)

@broker_bp.route('/broker/<int:broker_id>')
def view_broker(broker_id):
    broker = Broker.get_by_id(broker_id)
    stocks = Broker.get_stocks(broker_id)
    return render_template('broker_detail.html', broker=broker, stocks=stocks)

@broker_bp.route('/broker/create', methods=['GET', 'POST'])
def create_broker():
    if request.method == 'POST':
        name = request.form.get('name')
        commission_rate = request.form.get('commission_rate')
        license_number = request.form.get('license_number')
        stock_ids = request.form.getlist('stock_ids')
        
        broker_id = Broker.create(name, commission_rate, license_number)
        
        for stock_id in stock_ids:
            Broker.add_stock(broker_id, stock_id)
        
        return redirect(url_for('broker.list_brokers'))
    
    stocks = Stock.get_all()
    return render_template('broker_create.html', stocks=stocks)

@broker_bp.route('/broker/<int:broker_id>/add_stock', methods=['POST'])
def add_stock_to_broker(broker_id):
    stock_id = request.form.get('stock_id')
    Broker.add_stock(broker_id, stock_id)
    return redirect(url_for('broker.view_broker', broker_id=broker_id))

@broker_bp.route('/api/brokers')
def api_brokers():
    brokers = Broker.get_all()
    return jsonify([dict(broker) for broker in brokers])
