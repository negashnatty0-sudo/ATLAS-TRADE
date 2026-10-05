from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import db
from .models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return redirect(url_for("auth.register"))
        if User.query.filter_by(email=email).first():
            flash("Email already registered.")
            return redirect(url_for("auth.login"))
        u = User(email=email)
        u.set_password(password)
        db.session.add(u); db.session.commit()
        login_user(u)
        return redirect(url_for("main.dashboard"))
    return render_template("auth.html", mode="register")

@bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = User.query.filter_by(email=request.form["email"].strip().lower()).first()
        if u and u.check_password(request.form["password"]):
            login_user(u)
            return redirect(url_for("main.dashboard"))
        flash("Invalid email or password.")
    return render_template("auth.html", mode="login")

@bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
