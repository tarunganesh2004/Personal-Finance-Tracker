from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, User
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required

auth_blueprint = Blueprint("auth", __name__)
bcrypt = Bcrypt()


@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data["email"]
    password = data["password"]

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if user and bcrypt.check_password_hash(user.password, data["password"]):
        login_user(user)
        return jsonify({"message": "Logged in successfully!"}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@auth_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"}), 200
