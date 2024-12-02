from flask import render_template, redirect, url_for, request
from app.products import products_bp
from app.products.models import Product
from app.products.forms import CreateProductForm
from app import db

@products_bp.route('/productos', methods=['GET', 'POST'])
def productos():
    message = request.args.get('message', None)
    form = CreateProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data
        )
        db.session.add(new_product)
        db.session.commit()

    products = Product.query.all()
    return render_template(
        'products.html', 
        products=products, 
        form=form,
        message=message
    )

@products_bp.route('/producto/<int:id>', methods=['POST'])
def actualizar_stock(id):
    stock = request.form.get('stock')
    product = Product.query.get_or_404(id)
    product.stock = stock
    db.session.commit()
    return redirect(url_for('products.productos', message='Stock actualizado correctamente'))
