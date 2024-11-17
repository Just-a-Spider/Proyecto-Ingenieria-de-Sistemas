from app import db
from flask_login import UserMixin
from datetime import datetime
#models para usuarios
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # The role can only be: 'Admin', 'Vendedor'
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.role = 'Vendedor'

    def __repr__(self):
        return f'<User {self.username}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self