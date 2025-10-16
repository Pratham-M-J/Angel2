from flask import Flask, render_template
from routes.stock import stock_bp
from routes.trader import trader_bp
from routes.order import order_bp
from routes.broker import broker_bp
from routes.fo import fo_bp

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

app.register_blueprint(stock_bp)
app.register_blueprint(trader_bp)
app.register_blueprint(order_bp)
app.register_blueprint(broker_bp)
app.register_blueprint(fo_bp)

@app.route('/')
def index():
    """Main page showing all sections"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
