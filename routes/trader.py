from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import Trader

trader_bp = Blueprint('trader', __name__)

@trader_bp.route('/traders')
def list_traders():
    traders = Trader.get_all()
    return render_template('traders.html', traders=traders)

@trader_bp.route('/trader/<int:dmat_account_number>')
def view_trader(dmat_account_number):
    trader = Trader.get_by_id(dmat_account_number)
    return render_template('trader_detail.html', trader=trader)

@trader_bp.route('/trader/create', methods=['GET', 'POST'])
def create_trader():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        phone_number = request.form.get('phone_number')
        mail_id = request.form.get('mail_id')
        
        dmat_account_number = Trader.create(name, age, phone_number, mail_id)
        return redirect(url_for('trader.list_traders'))
    
    return render_template('trader_create.html')

@trader_bp.route('/api/traders')
def api_traders():
    traders = Trader.get_all()
    return jsonify([dict(trader) for trader in traders])
