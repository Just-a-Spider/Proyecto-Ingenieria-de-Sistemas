from flask import render_template, request, url_for, redirect, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from app import app, lm, db, bc
from app.users.models import User
from app.users.forms import LoginForm, RegisterForm

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET':
        return render_template('auth/register.html', form=form)

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if the user already exists
        user = User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'User already exists'
            return render_template('auth/register.html', form=form, msg=msg)
        else:
            new_user = User(
                username=username,
                email=email,
                password=bc.generate_password_hash(password).decode('utf-8')
            )
            new_user.save()
            return redirect(url_for('login'))
    else:
        msg = 'Please fill out the form'
        return render_template('auth/register.html', form=form, msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm(request.form)

    if request.method == 'GET':
        return render_template('auth/login.html', form=form)
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bc.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('products.products'))
        
        return abort(401)
    
    return render_template('auth/login.html', form=form)