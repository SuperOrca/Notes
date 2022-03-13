from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        logout_user()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password_hash, password):
                flash("Sucessfully logged in!", category="success")
                login_user(user, remember=bool(request.form.get("remember")))
                return redirect(url_for("user.notes"))
            else:
                flash("Incorrect password, try again.", category="danger")
        else:
            flash("Email not found, try again.", category="danger")

        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        logout_user()

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if len(username) > 15:
            flash("Username must be 15 characters or less.", category="danger")
        elif len(username) < 3:
            flash("Username must be 3 characters or more.", category="danger")
        # elif not char_check(username):
        #     flash("Username must not contain special characters.", category="danger")
        elif len(password) < 6:
            flash("Password must be at least 6 characters.", category="danger")
        elif len(password) > 32:
            flash("Password must be 32 characters or less.", category="danger")
        elif password != confirm:
            flash("Passwords do not match.", category="danger")
        elif User.query.filter_by(email=email).first():
            flash("Email already registered.", category="danger")
        elif User.query.filter_by(username=username).first():
            flash("Username already taken.", category="danger")
        else:
            password_hash = generate_password_hash(password, method="sha256")
            user = User(username=username, email=email, password_hash=password_hash)
            db.session.add(user)
            db.session.commit()

            login_user(user, remember=bool(request.form.get("remember")))
            flash("Account created!", category="success")
            return redirect(url_for("user.notes"))

    return render_template("register.html")
