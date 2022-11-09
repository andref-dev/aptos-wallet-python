from app_data import AppData
from models.users import User


def get_balance(app_data: AppData, user_id):
    user: User = app_data.users.get(user_id)
    balance = app_data.rest_client.account_balance(user.account.address())
    return {"balance": balance}


def fund_user(app_data: AppData, user_id, amount):
    user: User = app_data.users.get(user_id)
    app_data.faucet_client.fund_account(user.account.address(), amount)
    balance = app_data.rest_client.account_balance(user.account.address())
    return {"balance": balance}


def transfer_main_coin(app_data: AppData, user_from_id, user_to_id, amount):
    user_from: User = app_data.users.get(user_from_id)
    user_to: User = app_data.users.get(user_to_id)

    tx_hash = app_data.rest_client.transfer(
        user_from.account, user_to.account.address(), amount)

    app_data.rest_client.wait_for_transaction(tx_hash)

    sender_balance = app_data.rest_client.account_balance(
        user_from.account.address())
    receiver_balance = app_data.rest_client.account_balance(
        user_to.account.address())

    return {
        "sender_balance": sender_balance,
        "receiver_balance": receiver_balance
    }
