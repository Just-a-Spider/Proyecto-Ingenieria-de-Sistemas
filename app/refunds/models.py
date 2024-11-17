from app import db
from datetime import datetime

class Refund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # Foreign keys
    order_uuid = db.Column(db.String(36), db.ForeignKey('order.uuid'), nullable=False)

    # Relationships
    order = db.relationship('Order', backref='refunds', lazy=True)
