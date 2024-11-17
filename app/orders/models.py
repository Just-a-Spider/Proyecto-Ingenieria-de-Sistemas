from app import db

class Client(db.Model):
    dni = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(9), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)

    # Relationships
    orders = db.relationship('Order', backref='client', lazy=True)

class Order(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # The status can only be: 'Pendiente', 'Enviado', 'Cancelado'
    total = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(10), nullable=False)  # The payment method can only be: 'Efectivo', 'Tarjeta de crédito', 'Tarjeta de débito'

    # Foreign keys
    client_dni = db.Column(db.String(8), db.ForeignKey('client.dni'), nullable=False)  # Many orders can belong to one client

    # Relationships
    order_details = db.relationship('OrderDetail', backref='order', lazy=True)

class OrderDetail(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    # Foreign keys
    order_uuid = db.Column(db.String(36), db.ForeignKey('order.uuid'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    # Relationships
    product = db.relationship('Product', backref='order_details', lazy=True)