from flask import Blueprint
from flask_login import login_required

orders_bp = Blueprint('orders', __name__)

@orders_bp.before_request
@login_required
def before_request():
    pass

from app.orders import views