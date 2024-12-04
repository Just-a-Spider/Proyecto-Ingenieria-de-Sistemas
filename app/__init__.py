import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('app.config.Config')

db = SQLAlchemy(app)
bc = Bcrypt(app)
migrate = Migrate(app, db)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'users.login'  # Set the login view for the login_required decorator

# Import blueprints
from app.users import users_bp
from app.products import products_bp
from app.orders import orders_bp
from app.refunds import refunds_bp
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(refunds_bp)

@app.route('/')
def hello_world():
    return render_template('index.html')