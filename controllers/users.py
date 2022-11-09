from aptos_sdk.account import Account

from app_data import AppData
from models.users import User


def create_user(app_data: AppData, name):
    user = User(name)
    # Step needed so this account can interact with this resource later
    app_data.faucet_client.fund_account(user.account.address(), 0)
    app_data.users[str(user.id)] = user
    return user.to_dict()


def get_all_users(app_data: AppData):
    res = []
    for user in app_data.users.values():
        res.append(user.to_dict())

    return res


def get_user(app_data: AppData, user_id):
    user = app_data.users.get(user_id)
    return user.to_dict()
