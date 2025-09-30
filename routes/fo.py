from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import FuturesOptions, Stock

fo_bp = Blueprint('fo', __name__)

@fo_bp.route('/futures-options')
def list_fo():
    fos = FuturesOptions.get_all()
    return render_template('fo_list.html', fos=fos)

@fo_bp.route('/futures-options/<int:fo_id>')
def view_fo(fo_id):
    fo = FuturesOptions.get_by_id(fo_id)
    return render_template('fo_detail.html', fo=fo)

@fo_bp.route('/futures-options/create', methods=['GET', 'POST'])
def create_fo():
    if request.method == 'POST':
        fo_type = request.form.get('type')
        contract_size = request.form.get('contract_size')
        underlying_asset = request.form.get('underlying_asset')
        expiry_date = request.form.get('expiry_date')
        derivatives = request.form.get('derivatives') or None
        
        fo_id = FuturesOptions.create(fo_type, contract_size, underlying_asset, expiry_date, derivatives)
        return redirect(url_for('fo.list_fo'))
    
    stocks = Stock.get_all()
    return render_template('fo_create.html', stocks=stocks)

@fo_bp.route('/api/futures-options')
def api_fo():
    fos = FuturesOptions.get_all()
    return jsonify([dict(fo) for fo in fos])
