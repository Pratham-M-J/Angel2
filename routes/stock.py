from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import Stock

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/stocks')
def list_stocks():
    stocks = Stock.get_all()
    return render_template('stocks.html', stocks=stocks)

@stock_bp.route('/stock/<int:stock_id>')
def view_stock(stock_id):
    stock = Stock.get_by_id(stock_id)
    return render_template('stock_detail.html', stock=stock)

@stock_bp.route('/stock/create', methods=['GET', 'POST'])
def create_stock():
    if request.method == 'POST':
        stock_name = request.form.get('stock_name')
        stock_price = request.form.get('stock_price')
        pe_ratio = request.form.get('pe_ratio')
        
        stock_id = Stock.create(stock_name, stock_price, pe_ratio)
        return redirect(url_for('stock.list_stocks'))
    
    return render_template('stock_create.html')

@stock_bp.route('/api/stocks')
def api_stocks():
    stocks = Stock.get_all()
    return jsonify([dict(stock) for stock in stocks])
