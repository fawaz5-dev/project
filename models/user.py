from flask_login import UserMixin
from models import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'  # ✅ explicitly set table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


    # One-to-many: A user can have many clients
    clients = db.relationship('Client', backref='user', lazy=True)

    # Optional: A user can also have many FAQs (directly, if needed)
    faqs = db.relationship('FAQ', backref='user', lazy=True)

