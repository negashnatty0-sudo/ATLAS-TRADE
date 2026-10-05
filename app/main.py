from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .models import Trade, Backtest

bp = Blueprint("main", __name__)

@bp.get("/")
def index():
    return redirect(url_for("main.dashboard")) if current_user.is_authenticated else redirect(url_for("auth.login"))

@bp.get("/dashboard")
@login_required
def dashboard():
    trades = Trade.query.filter_by(user_id=current_user.id).order_by(Trade.opened_at.desc()).limit(20).all()
    return render_template("dashboard.html", trades=trades)

@bp.get("/admin")
@login_required
def admin():
    if not current_user.is_admin:
        return "Forbidden", 403
    from .models import User
    return render_template("admin.html", users=User.query.order_by(User.created_at.desc()).all())

@bp.get("/journal")
@login_required
def journal():
    return render_template("journal.html", trades=Trade.query.filter_by(user_id=current_user.id).order_by(Trade.opened_at.desc()).all())

@bp.get("/pricing")
def pricing():
    return render_template("pricing.html")
