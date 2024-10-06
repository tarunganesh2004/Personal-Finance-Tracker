from flask import Flask, jsonify, request, session, redirect, url_for
from models import db, User, Transaction
from auth import auth_blueprint
from flask_login import LoginManager, login_required, current_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Register auth routes for login, logout, register
app.register_blueprint(auth_blueprint)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/transactions", methods=["GET"])
@login_required
def get_transactions():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return jsonify([trans.to_dict() for trans in transactions])


@app.route("/transactions", methods=["POST"])
@login_required
def add_transaction():
    data = request.json
    new_transaction = Transaction(
        description=data["description"], amount=data["amount"], user_id=current_user.id
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify(new_transaction.to_dict()), 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if not exist
    app.run(debug=True)
