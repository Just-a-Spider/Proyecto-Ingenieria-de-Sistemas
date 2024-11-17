from flask import render_template, request, redirect, url_for
from app.products import products_bp
from app.products.models import Product
from app.products.forms import CreateProductForm
from app import db

@products_bp.route('/products', methods=['GET', 'POST'])
def products():
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
        return redirect(url_for('products.products'))

    products = Product.query.all()
    return render_template('products.html', products=products, form=form)