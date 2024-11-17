from flask import render_template
from app.refunds import refunds_bp
from app.refunds.models import Refund

@refunds_bp.route('/reembolsos')
def reembolsos():
    refunds = Refund.query.all()
    return render_template('reembolsos.html', refunds=refunds)