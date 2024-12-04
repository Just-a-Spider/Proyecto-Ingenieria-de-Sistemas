from flask import render_template, redirect, url_for, flash, request
from app.orders import orders_bp
from app.orders.models import Order, Client, OrderDetail
from app.orders import forms
from app.products.models import Product
from app.refunds.models import Refund
from app import db

@orders_bp.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    client_form = forms.CreateClientForm()
    order_form = forms.CreateOrderForm()
    clients = Client.query.all()

    if order_form.validate_on_submit():
        new_order = Order(
            client_dni=order_form.client_dni.data,
            payment_method=order_form.payment_method.data,
        )
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('orders.pedidos'))

    orders = Order.query.all()

    # Add a field to orders if they have a refund
    for order in orders:
        order.refund = Refund.query.filter_by(order_uuid=order.uuid).first() is not None

    # Check if a refund was requested via an order_uuid in the URL
    order_uuid = request.args.get('order_uuid', None)
    refund = None
    if order_uuid:
        refund = Refund.query.filter_by(order_uuid=order_uuid).first()

    return render_template(
        'orders.html', 
        clients=clients,
        client_form=client_form,
        order_form=order_form,
        orders=orders,
        refund=refund
    )

@orders_bp.route('/pedido/<string:uuid>', methods=['GET', 'POST'])
def pedido(uuid):
    refund = request.args.get('refund', 'false').lower() == 'true'
    order = Order.query.get_or_404(uuid)
    order_detail_form = forms.CreateOrderDetailForm(order_uuid=uuid)
    order_details = OrderDetail.query.filter_by(order_uuid=uuid).all()

    if order_detail_form.validate_on_submit():
        product = Product.query.get(order_detail_form.product_id.data)
        if product.stock < order_detail_form.quantity.data:
            flash(f'No hay suficiente stock para el producto {product.name}', 'error')
            return redirect(url_for('orders.pedido', uuid=uuid, refund=refund))

        existing_order_detail = OrderDetail.query.filter_by(
            order_uuid=uuid,
            product_id=order_detail_form.product_id.data
        ).first()

        if existing_order_detail:
            existing_order_detail.quantity += order_detail_form.quantity.data
            existing_order_detail.subtotal += product.price * order_detail_form.quantity.data
        else:
            new_order_detail = OrderDetail(
                order_uuid=uuid,
                product_id=order_detail_form.product_id.data,
                quantity=order_detail_form.quantity.data,
                subtotal=product.price * order_detail_form.quantity.data
            )
            db.session.add(new_order_detail)

        product.stock -= order_detail_form.quantity.data
        order.total += product.price * order_detail_form.quantity.data
        db.session.commit()
        return redirect(url_for('orders.pedido', uuid=uuid, refund=refund))

    products = Product.query.all()
    clients = Client.query.all()

    return render_template(
        'order_detail.html', 
        order=order,
        clients=clients,
        products=products,
        order_details=order_details,
        order_detail_form=order_detail_form,
        refund=refund
    )

@orders_bp.route('/pedido/<string:uuid>/eliminar', methods=['POST'])
def eliminar_pedido(uuid):
    order = Order.query.get_or_404(uuid)
    order_details = OrderDetail.query.filter_by(order_uuid=uuid).all()
    for order_detail in order_details:
        product = Product.query.get(order_detail.product_id)
        product.stock += order_detail.quantity
        db.session.delete(order_detail)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('orders.pedidos'))

@orders_bp.route('/pedido/<string:uuid>/eliminar/<string:order_detail_uuid>', methods=['POST'])
def eliminar_detalle_pedido(uuid, order_detail_uuid):
    order_detail = OrderDetail.query.get_or_404(order_detail_uuid)
    product = Product.query.get(order_detail.product_id)
    order = Order.query.get_or_404(uuid)
    order.total -= order_detail.subtotal
    product.stock += order_detail.quantity
    db.session.delete(order_detail)
    db.session.commit()
    return redirect(url_for('orders.pedido', uuid=uuid))

@orders_bp.route('/clientes', methods=['POST'])
def clientes():
    client_form = forms.CreateClientForm()
    if client_form.validate_on_submit():
        new_client = Client(
            dni=client_form.dni.data,
            name=client_form.name.data,
            email=client_form.email.data,
            phone=client_form.phone.data
        )
        db.session.add(new_client)
        db.session.commit()
    return redirect(url_for('orders.pedidos'))

@orders_bp.route('/cliente/<string:dni>/eliminar', methods=['POST'])
def eliminar_cliente(dni):
    client = Client.query.get_or_404(dni)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('orders.pedidos'))
