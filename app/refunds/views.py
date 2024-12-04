from flask import render_template, redirect, url_for, request
from app.refunds import refunds_bp
from app.refunds.models import Refund
from app import db

@refunds_bp.route('/reembolsos', methods=['GET', 'POST'])
def reembolsos():
    refunds = Refund.query.all()
    if refunds == None:
        # Si no hay reembolsos, retornar una lista vacía
        refunds = []

    return render_template('refunds.html', refunds=refunds)

@refunds_bp.route('/reembolsos/<string:uuid>')
def reembolso(uuid):
    refund = Refund.query.filter_by(order_uuid=uuid).first()
    return render_template('refund.html', refund=refund)

@refunds_bp.route('/reembolsos/nuevo/<string:uuid>', methods=['POST'])
def nuevo_reembolso(uuid):
    # Get the data form the orders_partial.html form
    reason = request.form['reason']
    refund = Refund(reason=reason, order_uuid=uuid)
    db.session.add(refund)
    db.session.commit()
    return redirect(url_for('refunds.reembolsos'))


