from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import InputRequired
from app.orders.models import Client  # Import the Client model
from app.products.models import Product  # Import the Product model

class CreateClientForm(FlaskForm):
    dni = StringField('DNI', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired()])

class CreateOrderForm(FlaskForm):
    client_dni = SelectField('Client DNI', validators=[InputRequired()], coerce=str)
    payment_method = SelectField('Payment Method', validators=[InputRequired()], choices=[
        ('Efectivo', 'Efectivo'),
        ('Yape', 'Yape'),
        ('Tarjeta', 'Tarjeta')
    ])

    def __init__(self, *args, **kwargs):
        super(CreateOrderForm, self).__init__(*args, **kwargs)
        self.client_dni.choices = [(client.dni, client.dni) for client in Client.query.all()]

class CreateOrderDetailForm(FlaskForm):
    order_uuid = StringField('Order UUID', validators=[InputRequired()])
    product_id = SelectField('Product ID', validators=[InputRequired()], coerce=str)
    quantity = IntegerField('Quantity', validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        super(CreateOrderDetailForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(product.id, f'{product.name} - {product.stock}') for product in Product.query.all()]
