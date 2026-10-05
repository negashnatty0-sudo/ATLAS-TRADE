from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    trades = db.relationship("Trade", backref="user", lazy=True, cascade="all, delete-orphan")
    def set_password(self, p): self.password_hash = generate_password_hash(p)
    def check_password(self, p): return check_password_hash(self.password_hash, p)

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    symbol = db.Column(db.String(32), nullable=False)
    side = db.Column(db.String(8), nullable=False)
    entry = db.Column(db.Float, nullable=False)
    exit = db.Column(db.Float)
    quantity = db.Column(db.Float, default=1)
    stop_loss = db.Column(db.Float)
    take_profit = db.Column(db.Float)
    pnl = db.Column(db.Float, default=0)
    notes = db.Column(db.Text, default="")
    opened_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime)

class Backtest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    symbol = db.Column(db.String(32), nullable=False)
    strategy = db.Column(db.String(120), nullable=False)
    result_json = db.Column(db.Text, default="{}")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    plan = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(32), default="pending")
    provider_customer_id = db.Column(db.String(255))
    provider_subscription_id = db.Column(db.String(255), unique=True)
    current_period_end = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
