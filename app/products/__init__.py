from flask import Blueprint
from flask_login import login_required

products_bp = Blueprint('products', __name__)

@products_bp.before_request
@login_required
def before_request():
    pass

from app.products import views