from flask import Flask, jsonify, request

from controllers.users import create_user, get_all_users, get_user
from controllers.coins import fund_user, get_balance, transfer_main_coin
from controllers.nfts import (
    create_collection, get_all_collections, get_collection_data,
    get_all_tokens, create_token, get_token_balance, get_token_data, transfer_token
)
from app_data import AppData

app = Flask(__name__)

app_data = AppData()


@app.errorhandler(404)
def page_not_found(e):
    return "Not found :("


@app.route("/health")
def hello_world():
    return jsonify({"status": "pass"})


@app.route("/users", methods=["POST", "GET"])
def users():
    if request.method == "POST":
        content = request.get_json()
        user = create_user(app_data, content["name"])
        return jsonify(user)
    else:
        res = get_all_users(app_data)
        return jsonify(res)


@app.route("/users/<user_id>", methods=["GET"])
def get_user_route(user_id):
    res = get_user(app_data, user_id)
    return jsonify(res)


@app.route("/coin/balance", methods=["GET"])
def get_user_balance_route():
    content = request.get_json()
    res = get_balance(app_data, content["user_id"])
    return jsonify(res)


@app.route("/coin/fund", methods=["POST"])
def fund_user_route():
    content = request.get_json()
    res = fund_user(app_data, content["user_id"], content["amount"])
    return jsonify(res)


@app.route("/coin/transfer", methods=["POST"])
def transfer_coin_route():
    content = request.get_json()
    user_id_from = content["user_from"]
    user_id_to = content["user_to"]
    amount = content["amount"]

    res = transfer_main_coin(app_data, user_id_from, user_id_to, amount)
    return jsonify(res)


@app.route("/nfts", methods=["POST", "GET"])
def nft_collection_routes():
    if request.method == "POST":
        content = request.get_json()
        res = create_collection(
            app_data, content["creator_id"], content["name"], content["description"], content["url"])
        return jsonify(res)
    else:
        res = get_all_collections(app_data)
        return jsonify(res)


@app.route("/nfts/<collection_id>", methods=["GET", "POST"])
def get_collection_data_route(collection_id):
    if request.method == "POST":
        content = request.get_json()
        user_to = content["user_to"]
        name = content["name"]
        description = content["description"]
        url = content["url"]
        amount = content["amount"]
        res = create_token(app_data, collection_id,
                           user_to, name, description, url, amount)
        return jsonify(res)
    else:
        res = get_collection_data(app_data, collection_id)
        return jsonify(res)


@app.route("/nfts/tokens", methods=["GET"])
def get_tokens_routes():
    res = get_all_tokens(app_data)
    return jsonify(res)


@app.route("/nfts/tokens/<token_id>", methods=["GET"])
def get_token_route(token_id):
    res = get_token_data(app_data, token_id)
    return jsonify(res)


@app.route("/nfts/tokens/<token_id>/balance/<user_id>", methods=["GET"])
def get_token_balance_route(token_id, user_id):
    res = get_token_balance(app_data, token_id, user_id)
    return jsonify(res)


@app.route("/nfts/tokens/<token_id>/transfer", methods=["POST"])
def transfer_token_route(token_id):
    content = request.get_json()
    sender_id = content["user_from"]
    receiver_id = content["user_to"]
    amount = content["amount"]
    res = transfer_token(app_data, token_id, sender_id, receiver_id, amount)
    return jsonify(res)
