from flask import Flask, jsonify, request, url_for  # noqa: F401
from service.models import db, Account
from service.common import status

app = Flask(__name__)

# -------------------------------
# GET all accounts
# -------------------------------
@app.route("/accounts", methods=["GET"])
def get_accounts():
    accounts = Account.query.all()
    results = [account.serialize() for account in accounts]
    return jsonify(results), status.HTTP_200_OK

# -------------------------------
# GET account by ID
# -------------------------------
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), status.HTTP_404_NOT_FOUND
    return jsonify(account.serialize()), status.HTTP_200_OK

# -------------------------------
# CREATE a new account
# -------------------------------
@app.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), status.HTTP_400_BAD_REQUEST

    account = Account(
        name=data.get("name"),
        email=data.get("email"),
        address=data.get("address"),
        phone_number=data.get("phone_number")
    )
    db.session.add(account)
    db.session.commit()
    return jsonify(account.serialize()), status.HTTP_201_CREATED

# -------------------------------
# UPDATE an existing account
# -------------------------------
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), status.HTTP_404_NOT_FOUND

    data = request.get_json()
    account.name = data.get("name", account.name)
    account.email = data.get("email", account.email)
    account.address = data.get("address", account.address)
    account.phone_number = data.get("phone_number", account.phone_number)

    db.session.commit()
    return jsonify(account.serialize()), status.HTTP_200_OK

# -------------------------------
# DELETE an account
# -------------------------------
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), status.HTTP_404_NOT_FOUND

    db.session.delete(account)
    db.session.commit()
    return "", status.HTTP_204_NO_CONTENT

# -------------------------------
# Health check route
# -------------------------------
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), status.HTTP_200_OK

# -------------------------------
# Additional routes from main branch
# -------------------------------
# Example: search endpoint
# @app.route("/accounts/search", methods=["GET"])
# def search_accounts():
#     query = request.args.get("q")
#     results = Account.query.filter(Account.name.ilike(f"%{query}%")).all()
#     return jsonify([a.serialize() for a in results]), status.HTTP_200_OK

# -------------------------------
# App initialization
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
