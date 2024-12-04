from flask import Blueprint
from flask_login import login_required

refunds_bp = Blueprint('refunds', __name__)

@refunds_bp.before_request
@login_required
def before_request():
    pass

from app.refunds import views
