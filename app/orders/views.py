from flask import render_template
from app.orders import orders_bp
from app.orders.models import Order

@orders_bp.route('/pedidos')
def pedidos():
    orders = Order.query.all()
    return render_template('pedidos.html', orders=orders)