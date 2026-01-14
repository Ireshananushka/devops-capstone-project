from flask import request, jsonify, make_response, abort
from service.models import Account
from service.common import status
from . import app


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), status.HTTP_200_OK


@app.route("/")
def index():
    return jsonify(
        name="Account REST API Service",
        version="1.0",
    ), status.HTTP_200_OK


@app.route("/accounts", methods=["POST"])
def create_accounts():
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()

    message = account.serialize()
    location_url = f"/accounts/{account.id}"

    return make_response(
        jsonify(message),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


@app.route("/accounts", methods=["GET"])
def list_accounts():
    accounts = Account.all()
    return jsonify([account.serialize() for account in accounts]), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, "Account not found")
    return jsonify(account.serialize()), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, "Account not found")
    account.deserialize(request.get_json())
    account.update()
    return jsonify(account.serialize()), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", status.HTTP_204_NO_CONTENT


def check_content_type(media_type):
    content_type = request.headers.get("Content-Type")
    if content_type == media_type:
        return
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
